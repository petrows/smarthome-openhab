/**
 * @file 3D printers control rules (Bambu P2S).
 *
 * Printer state is mirrored to the GDA015 backlight:
 * - Backlight is on while the printer is connected.
 * - Backlight color reflects the current gcode state.
 * - Printer temperature and progress are forwarded to the GDA015 display.
 */

const { rules, triggers, items } = require('openhab');

/** Printer is switched off after this idle time, seconds. */
const IDLE_TIMEOUT = 3600;

/** Gcode state -> backlight HSB color. */
const GCODE_STATE_COLORS = {
    FINISH: '120,100,70', // green
    PREPARE: '0,0,70', // white
    RUNNING: '37,100,70', // yellow
    FAILED: '0,100,70', // red
};

/** Backlight color for all other gcode states: blue. */
const DEFAULT_COLOR = '240,100,70';

// Track P2S idle status and switch off with too long state
rules.JSRule({
    name: 'P2S Idle check',
    id: 'p2s-idle-check',
    triggers: [triggers.ItemStateUpdateTrigger('p2s_idle_time')],
    execute: () => {
        if (items.getItem('p2s_connected').state === 'OFF') {
            // Ignore disconnected device
            items.getItem('gda015_bkl_sw').sendCommand('OFF');
            return;
        }

        const idleValue = items.getItem('p2s_idle_time').numericState;
        if (idleValue > IDLE_TIMEOUT) {
            console.info(`P2S Idle check: device is idle for ${idleValue} seconds, switch off`);
            items.getItem('bambu_p2s_power_sw').sendCommand('OFF');
            items.getItem('gda015_bkl_sw').sendCommand('OFF');
        }
    },
});

// Connected state
rules.JSRule({
    name: 'P2S Connection status update',
    id: 'p2s-connection-status-update',
    triggers: [triggers.ItemStateUpdateTrigger('p2s_connected')],
    execute: (event) => {
        items.getItem('gda015_bkl_sw').sendCommand(event.receivedState);
    },
});

// Working state: set backlight color by gcode state
rules.JSRule({
    name: 'P2S Connection gcode update',
    id: 'p2s-connection-gcode-update',
    triggers: [triggers.ItemStateChangeTrigger('p2s_gcode_state')],
    execute: (event) => {
        const color = GCODE_STATE_COLORS[event.newState] || DEFAULT_COLOR;
        console.info(`P2S Connection gcode update: state ${event.newState}, color ${color}`);
        items.getItem('gda015_bkl_color').sendCommand(color);
    },
});

// Update printer metrics data
rules.JSRule({
    name: 'P2S Temperature update',
    id: 'p2s-temperature-update',
    triggers: [triggers.ItemStateUpdateTrigger('p2s_temperature_tool_actual')],
    execute: () => {
        items.getItem('gda015_temperature').sendCommand(items.getItem('p2s_temperature_tool_actual').quantityState);
    },
});

rules.JSRule({
    name: 'P2S Progress update',
    id: 'p2s-progress-update',
    triggers: [triggers.ItemStateUpdateTrigger('p2s_progress')],
    execute: () => {
        items.getItem('gda015_progress').sendCommand(items.getItem('p2s_progress').numericState);
    },
});
