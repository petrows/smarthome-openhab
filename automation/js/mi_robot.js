/**
 * @file Vacuum robot rules (ROIDMI EVE, miio binding).
 *
 * The house has several identical robots, so all rules are generated per
 * robot from the `ROBOTS` config below. Item names are derived from the
 * robot key as `<key>_robot_<suffix>` (see items/mi-robot.items).
 *
 * Per robot the following rules are created:
 * - Custom command: translates UI commands (FIND/START/STOP/RETURN/SUCK)
 *   from `<key>_robot_custom_command` into miio actions.
 * - Status text: maps the numeric robot status to human-readable text.
 * - Error: maps the fault code to text and sends a notification.
 * - Clean auto: scheduled regular cleaning with sanity checks.
 */

const { rules, triggers, items, actions } = require('openhab');

/** Per-robot configuration; `key` is the item name prefix. */
const ROBOTS = [
    { key: 'eg', label: 'EG', cleanCron: '0 30 13 ? * MON-FRI' },
    { key: 'kg', label: 'KG', cleanCron: '0 0 06 ? * MON-FRI' },
];

/** UI command -> miio binding action. */
const CUSTOM_COMMANDS = {
    FIND: 'custom-find-robot',
    START: 'vacuum-start-sweep',
    STOP: 'vacuum-stop-sweeping',
    RETURN: 'battery-start-charge',
    SUCK: 'custom-start-dust',
};

/** Robot status code "Sweeping", see eve_status.map. */
const STATUS_SWEEPING = 4;

/** Sweep level 100%, see eve_level.map. */
const SWEEP_LEVEL_MAX = 4;

/** Returns the robot's item `<key>_robot_<suffix>`. */
const robotItem = (robot, suffix) => items.getItem(`${robot.key}_robot_${suffix}`);

ROBOTS.forEach((robot) => {
    rules.JSRule({
        name: `${robot.label} Robot custom command`,
        id: `${robot.key}-robot-custom-command`,
        triggers: [triggers.ItemCommandTrigger(`${robot.key}_robot_custom_command`)],
        execute: (event) => {
            console.warn(`${robot.label} Robot custom command: ${event.receivedCommand}`);

            const action = CUSTOM_COMMANDS[event.receivedCommand];
            if (action) {
                robotItem(robot, 'actions').sendCommand(action);
            }

            // Reset button status to empty
            robotItem(robot, 'custom_command').postUpdate('');
        },
    });

    rules.JSRule({
        name: `${robot.label} Robot status text`,
        id: `${robot.key}-robot-status-text`,
        triggers: [triggers.ItemStateChangeTrigger(`${robot.key}_robot_status`)],
        execute: () => {
            const statusText = actions.Transformation.transform(
                'MAP', 'eve_status.map', robotItem(robot, 'status').state);
            robotItem(robot, 'status_text').sendCommand(statusText);
        },
    });

    rules.JSRule({
        name: `${robot.label} Robot error`,
        id: `${robot.key}-robot-error`,
        triggers: [triggers.ItemStateChangeTrigger(`${robot.key}_robot_fault`)],
        execute: () => {
            const errorText = actions.Transformation.transform(
                'MAP', 'eve_fault.map', robotItem(robot, 'fault').state);

            robotItem(robot, 'fault_text').sendCommand(errorText);

            items.getItem('global_message').sendCommand(`${robot.label} Robot error: ${errorText}`);
        },
    });

    // Regular cleaning
    rules.JSRule({
        name: `${robot.label} Robot clean auto`,
        id: `${robot.key}-robot-clean-auto`,
        triggers: [triggers.GenericCronTrigger(robot.cleanCron)],
        execute: () => {
            const globalMessage = items.getItem('global_message');

            // Master switch
            if (robotItem(robot, 'regular_enable').state === 'OFF') {
                console.warn(`${robot.label} Robot regular clean disabled`);
                return;
            }

            // Check valid status (no faults)
            if (robotItem(robot, 'fault').numericState !== 0) {
                const faultText = robotItem(robot, 'fault_text').state;
                console.warn(`${robot.label} Robot regular clean skipped: robot fault ${faultText}`);
                globalMessage.sendCommand(`${robot.label} Robot clean skipped, error: ${faultText}`);
                return;
            }

            // Check valid status (already running)
            if (robotItem(robot, 'status').numericState === STATUS_SWEEPING) {
                console.warn(`${robot.label} Robot regular clean skipped: robot already active`);
                globalMessage.sendCommand(`${robot.label} Robot clean skipped: robot already active`);
                return;
            }

            const x2Mode = robotItem(robot, 'regular_x2').state;
            console.warn(`${robot.label} Robot regular clean started, x2 mode: ${x2Mode}`);

            robotItem(robot, 'double_clean').sendCommand(x2Mode);
            robotItem(robot, 'sweep_level').sendCommand(SWEEP_LEVEL_MAX);
            robotItem(robot, 'custom_command').sendCommand('START');
        },
    });
});
