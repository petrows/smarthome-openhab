/**
 * @file Strips embedded line breaks from String item states.
 *
 * A raw newline inside a String value breaks the InfluxDB line protocol used
 * by the InfluxDB persistence add-on (one data point per line): vmagent then
 * rejects the whole write batch, not just the offending point. This can come
 * from any source - a manual postUpdate, an upstream API quirk, a copy-paste
 * - so instead of fixing it per item, every String item is cleaned here.
 */

const { rules, triggers, items } = require('openhab');

// Stateless test regex (no /g/, so .test() is safe to reuse across calls)
const HAS_LINE_BREAK = /[\r\n]/;

rules.JSRule({
    name: 'Sanitize string item line breaks',
    id: 'sanitize-string-items',
    triggers: [
        triggers.GenericEventTrigger('openhab/items/**', '', 'ItemStateChangedEvent', 'sanitize-string-items-all'),
    ],
    execute: (event) => {
        if (event.payload.type !== 'String') return;

        const value = event.payload.value;
        if (!HAS_LINE_BREAK.test(value)) return;

        const cleaned = value.replace(/[\r\n]+/g, ' ').trim();
        console.warn(`Sanitize: item ${event.itemName} contained a line break, cleaned: "${cleaned}"`);
        items.getItem(event.itemName).postUpdate(cleaned);
    },
});
