/**
 * @file Device activity watchdog.
 *
 * Once a day (13:00) walks over all members of the `g_all_activity` group
 * (DateTime items holding the last activity timestamp of a device) and sends
 * a notification via the `global_message` item for every device that:
 * - was not updated within the last 24 hours, or
 * - has no known last update time at all (state is NULL/UNDEF).
 */

const { rules, triggers, items, time } = require('openhab');

/** Maximum allowed device silence before a notification is sent, hours. */
const MAX_SILENCE_HOURS = 24;

rules.JSRule({
    name: 'Test devices response time',
    id: 'test-devices-response-time',
    triggers: [triggers.GenericCronTrigger('0 00 13 ? * *')],
    execute: () => {
        const globalMessage = items.getItem('global_message');

        items.getItem('g_all_activity').members.forEach((item) => {
            // Last ping time is not known at all?
            if (item.isUninitialized) {
                console.info(`Item ${item.label} never updated`);
                globalMessage.sendCommand(`Item ${item.label} last activity time is unknown`);
                return;
            }

            const diffHours = time.toZDT(item).until(time.toZDT(), time.ChronoUnit.HOURS);

            console.info(`Item ${item.label} last update: ${diffHours} h ago`);

            if (diffHours > MAX_SILENCE_HOURS) {
                globalMessage.sendCommand(`Item ${item.label} no activity for ${diffHours} h`);
            }
        });
    },
});
