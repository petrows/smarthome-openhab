/**
 * @file Turns off the bedroom TV every night, in case someone forgot it on.
 */

const { rules, triggers, items } = require('openhab');

rules.JSRule({
    name: 'SZ TV night off',
    id: 'sz-tv-night-off',
    triggers: [triggers.GenericCronTrigger('0 00 04 ? * *')],
    execute: () => {
        const tvPower = items.getItem('sz_tv_power_sw');

        if (tvPower.state === 'ON') {
            console.info('SZ TV night off: TV was on, switching off');
            tvPower.sendCommand('OFF');
        }
    },
});
