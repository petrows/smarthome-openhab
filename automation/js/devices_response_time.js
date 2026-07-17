/**
 * @file Device activity watchdog.
 *
 * Once a day (13:00) walks over all members of the `g_all_activity` group
 * (DateTime items holding the last activity timestamp of a device) and sends
 * a single summary notification via the `global_message` item, listing all
 * devices that:
 * - were not updated within the last 24 hours, or
 * - have no known last update time at all (state is NULL/UNDEF).
 */

const { rules, triggers, items, time } = require('openhab');

/** Maximum allowed device silence before a notification is sent, hours. */
const MAX_SILENCE_HOURS = 24;

rules.JSRule({
    name: 'Test devices response time',
    id: 'test-devices-response-time',
    triggers: [triggers.GenericCronTrigger('0 00 13 ? * *')],
    execute: () => {
        const silent = [];
        const unknown = [];

        items.getItem('g_all_activity').members.forEach((item) => {
            // Last ping time is not known at all?
            if (item.isUninitialized) {
                console.info(`Item ${item.label} never updated`);
                unknown.push(item.label);
                return;
            }

            const diffHours = time.toZDT(item).until(time.toZDT(), time.ChronoUnit.HOURS);

            console.info(`Item ${item.label} last update: ${diffHours} h ago`);

            if (diffHours > MAX_SILENCE_HOURS) {
                silent.push(`${item.label}: ${diffHours} h`);
            }
        });

        if (silent.length === 0 && unknown.length === 0) {
            return;
        }

        // Single report message, one device per line
        const report = ['Device activity report'];
        if (silent.length > 0) {
            report.push('', 'No activity:', ...silent.map((line) => `- ${line}`));
        }
        if (unknown.length > 0) {
            report.push('', 'Never updated:', ...unknown.map((line) => `- ${line}`));
        }
        // Do not set \n in the item text!!! Breaks Influxdb
        items.getItem('global_message').sendCommand(report.join('\\n'));
    },
});
