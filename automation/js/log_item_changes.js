const { rules, triggers } = require('openhab');

rules.JSRule({
    name: 'Log all item state changes',
    id: 'log-all-item-changes',
    triggers: [
        triggers.GenericEventTrigger('openhab/items/**', '', 'ItemStateChangedEvent', 'all-item-changes'),
    ],
    execute: (event) => {
        // debugger;
        // console.info(`${event.itemName}: ${event.payload.oldValue} -> ${event.payload.value}`);
    },
});
