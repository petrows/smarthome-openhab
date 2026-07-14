/**
 * @file MQTT event bus — bridge between openHAB items and smart speakers
 * (e.g. Yandex via yandex2mqtt).
 *
 * Publishes every item state change to MQTT and accepts commands for any
 * item from MQTT, applying value conversions the speaker integrations need.
 *
 * ## State publishing (openHAB -> MQTT)
 *
 * Every `ItemStateChangedEvent` is published (retained) to:
 *
 *     eventbus/state/<item_name>            <value>
 *
 * Value normalization:
 * - Quantity states are published as a plain number, units stripped
 *   (`23.5 °C` -> `23.5`).
 * - Decimal/Percent states are rounded to an integer to avoid values like
 *   `54.05820133333333333333`.
 * - Everything else is published as-is (`ON`, `CLOSED`, `12,34,56`, ...).
 *
 * Items whose name ends with `_ct` (color temperature dimmers, 0..100 %)
 * additionally publish the value converted to Kelvin (needed for some
 * integrations, like Yandex):
 *
 *     eventbus/state/<item_name>/ct_k       <kelvin>
 *
 * ## Commands (MQTT -> openHAB)
 *
 * Commands arrive on the `mqtt:broker:openhab:eventbus` trigger channel as:
 *
 *     eventbus/set/<item_name>/<value_type>#<value>
 *
 * `<value_type>` selects the converter applied to `<value>` before it is
 * sent as a command to `<item_name>`:
 *
 * | value_type | Meaning                                                      |
 * |------------|--------------------------------------------------------------|
 * | `sw`       | Boolean-ish (`off`/`false`/`0` -> `OFF`, anything else `ON`) |
 * | `ct_k`     | Color temperature in Kelvin -> percent of the 150..500 mired range |
 * | `rgb_int`  | Color as 24-bit int (0xRRGGBB) -> HSB, brightness forced to 50 % |
 * | other      | Passed through unchanged                                     |
 *
 * Independent of `value_type`, a value prefixed with `+` or `-` is treated
 * as relative: the delta is applied to the item's current numeric state
 * (e.g. `#+10` on a dimmer at 40 % sends `50`).
 */

const { rules, triggers, items, actions } = require('openhab');

// Java types for HSB conversion
const HSBType = Java.type('org.openhab.core.library.types.HSBType');
const PercentType = Java.type('org.openhab.core.library.types.PercentType');

const MQTT_BROKER = 'mqtt:broker:openhab';

/** Command values (case-insensitive) mapped to `OFF` by the `sw` converter. */
const OFF_STATES = ['off', 'false', '0'];

/**
 * Handles `eventbus/set/...` messages from the broker trigger channel:
 * parses the topic, converts the value according to `value_type` and sends
 * it as a command to the target item.
 */
rules.JSRule({
    name: 'Eventbus command',
    id: 'eventbus-command',
    triggers: [triggers.ChannelEventTrigger('mqtt:broker:openhab:eventbus')],
    execute: (event) => {
        // Message: eventbus/set/item_id/value_type#value
        const [topic, rawValue] = event.receivedEvent.split('#');
        const topicParts = topic.split('/');

        if (topicParts[0] !== 'eventbus') return; // Ignore other commands

        const itemID = topicParts[2];
        const commandType = topicParts[3];
        let command = rawValue;

        console.info(`Command, item = ${itemID}, commandType = ${commandType}, command = ${command}`);

        // Bool true / false, 0 / 1 for ON / OFF?
        if (commandType === 'sw') {
            command = OFF_STATES.includes(command.toLowerCase()) ? 'OFF' : 'ON';
        }

        // Relative value?
        const prefixChar = command.charAt(0);
        if (prefixChar === '+' || prefixChar === '-') {
            // Correct value, using current state (numericState handles both Quantity and plain numbers)
            const currentValue = items.getItem(itemID).numericState;
            const commandValue = parseFloat(command.substring(1));

            command = (prefixChar === '-'
                ? currentValue - commandValue
                : currentValue + commandValue).toString();
        }

        // CT in Kelvin
        if (commandType === 'ct_k') {
            // Convert K -> MiRED
            const valueK = parseFloat(command);
            let valueMiRed = 1000000.0 / valueK;

            console.info(`CT/K converter: K = ${valueK}, MiRed = ${valueMiRed}`);

            valueMiRed = Math.min(500, Math.max(150, valueMiRed));

            // Calculate % in range 150...500
            command = Math.round((valueMiRed - 150) / (500 - 150) * 100.0).toString();
        }

        // RGB as 24-bit int
        if (commandType === 'rgb_int') {
            const valueInt = parseInt(command);
            const r = (valueInt >> 16) & 255;
            const g = (valueInt >> 8) & 255;
            const b = valueInt & 255;

            let hsbValue = HSBType.fromRGB(r, g, b);

            // Drop brightness to 50%
            hsbValue = new HSBType(hsbValue.getHue(), hsbValue.getSaturation(), new PercentType(50));

            console.info(`Color converter: Int = ${valueInt}, HSB = ${hsbValue}`);

            command = hsbValue.toString();
        }

        items.getItem(itemID).sendCommand(command);
    },
});

/**
 * Publishes every item state change to `eventbus/state/<item_name>`
 * (retained), normalizing the value; `*_ct` items also get a companion
 * `/ct_k` topic with the value converted to Kelvin.
 */
rules.JSRule({
    name: 'Eventbus status',
    id: 'eventbus-status',
    triggers: [
        triggers.GenericEventTrigger('openhab/items/**', '', 'ItemStateChangedEvent', 'eventbus-status-all'),
    ],
    execute: (event) => {
        const stateType = event.payload.type;
        let value = event.payload.value;

        // If Item with Units -> get raw value as double
        if (stateType === 'Quantity') {
            value = parseFloat(value).toString();
        } else if (stateType === 'Decimal' || stateType === 'Percent') {
            // If Dimmer/Number item -> round value to avoid 54.0582013333333333333333333333333300
            value = Math.round(parseFloat(value)).toString();
        }

        const mqtt = actions.get('mqtt', MQTT_BROKER);
        const topic = `eventbus/state/${event.itemName}`;
        mqtt.publishMQTT(topic, value, true);

        // Send second state for CT items - in Kelvin (need for some bindings, like Yandex)
        if (event.itemName.endsWith('_ct')) {
            const dim = parseFloat(value);
            const mired = 150 + (500 - 150) * (dim / 100.0);
            const kelvin = Math.round(1000000.0 / mired);
            mqtt.publishMQTT(`${topic}/ct_k`, kelvin.toString(), true);
        }
    },
});
