/**
 * @file Sunrise emulation.
 *
 * Gradually turns on the lamps of the `g_sunrise` group one after another
 * and shifts the color temperature from warm to cold, emulating a sunrise.
 *
 * Lamps are the `*_sw` members of `g_sunrise`, sorted by the `sunrise_order`
 * item metadata (lower value starts earlier; lamps without it go last, in
 * name order). Every lamp MUST have a matching `*_dim` item; a `*_ct` item
 * is optional (lamps without one just do not participate in the CT ramp).
 *
 * The full program runs SUNRISE_PERIOD_S seconds: each lamp in turn ramps
 * from 0 to 100 %, and the `*_ct` items ramp from 100 (warm) down to
 * 0 (cold) over the last part of the program (after CT_START_PROGRESS).
 *
 * A run stops early when `sunrise_enable` is switched OFF or when the user
 * switches all lamps of the group off after the ramp has started.
 */

const { rules, triggers, items } = require('openhab');

// === Configuration

/** How long the full program runs, seconds. */
const SUNRISE_PERIOD_S = 60 * 60;

/**
 * Brightness change on each step, percent.
 * Increase this value to reduce command traffic, decrease for better smooth.
 */
const BRIGHT_STEP_PERCENT = 1;

/** Overall progress (0..1) at which the CT ramp starts. */
const CT_START_PROGRESS = 0.6;

// === Configuration end

/** Currently scheduled step of a running emulation, if any. */
let sunriseTimer = null;

/** Sort key of a lamp: `sunrise_order` metadata value, unordered lamps go last. */
const orderOf = (item) => {
    const md = item.getMetadata('sunrise_order');
    return md ? parseFloat(md.value) : Number.MAX_SAFE_INTEGER;
};

/**
 * Returns the `{sw, dim, ct}` item triples of the `g_sunrise` lamps, sorted
 * by the `sunrise_order` metadata. Lamps without a `_dim` item are skipped,
 * `ct` is null for lamps without a `_ct` item.
 */
const sunriseLamps = () => items.getItem('g_sunrise').members
    .sort((a, b) => orderOf(a) - orderOf(b) || a.name.localeCompare(b.name))
    .map((sw) => {
        const base = sw.name.replace(/_sw$/, '');
        const dim = items.getItem(`${base}_dim`, true);
        if (!dim) {
            console.error(`Sunrise: no dimmer found for ${sw.name}, lamp skipped`);
        }
        return { sw, dim, ct: items.getItem(`${base}_ct`, true) };
    })
    .filter((lamp) => lamp.dim);

rules.JSRule({
    name: 'Sunrise emulation auto off',
    id: 'sunrise-auto-off',
    triggers: [triggers.ChannelEventTrigger('astro:sun:home:daylight#event', 'START')],
    execute: () => {
        console.warn('Sunrise emulation daylight switch off');

        if (items.getItem('sunrise_enable').state === 'OFF') {
            console.warn('Sunrise emulation disabled');
            return;
        }

        items.getItem('sz_light').sendCommand('OFF');
    },
});

rules.JSRule({
    name: 'Sunrise emulation start',
    id: 'sunrise-start',
    triggers: [
        triggers.GenericCronTrigger('0 00 05 ? * *'),
        triggers.ItemStateUpdateTrigger('test_sw_check_sunrize'),
    ],
    execute: () => {
        console.warn('Sunrise emulation started');

        if (items.getItem('sunrise_enable').state === 'OFF') {
            console.warn('Sunrise emulation disabled');
            return;
        }

        if (sunriseTimer !== null) {
            console.warn('Sunrise emulation: previous run cancelled');
            clearTimeout(sunriseTimer);
        }

        const lamps = sunriseLamps();
        if (lamps.length === 0) {
            console.error('Sunrise emulation: group g_sunrise is empty');
            return;
        }

        // Step period, so all lamps ramp 0 -> 100 % within SUNRISE_PERIOD_S
        const tickMs = (SUNRISE_PERIOD_S * 1000) / ((100 / BRIGHT_STEP_PERCENT) * lamps.length);

        // Last CT value sent to the lamps, to avoid re-sending it every tick
        let lastCt = null;

        /**
         * One dimming step. `brightness` is the overall program position
         * (0 .. lamps * 100); each lamp owns its 100 % wide segment of it.
         */
        const tick = (brightness, started) => {
            sunriseTimer = null;

            if (items.getItem('sunrise_enable').state === 'OFF') {
                console.warn('Sunrise emulation disabled');
                return;
            }

            // Group is OR(ON, OFF): not ON means the user switched all lamps off
            if (started && items.getItem('g_sunrise').state !== 'ON') {
                console.warn('Sunrise emulation stopped: group switched off');
                return;
            }

            const overallProgress = brightness / (lamps.length * 100);

            lamps.forEach((lamp, index) => {
                const setBright = brightness - index * 100;

                // Not this lamp's segment - skip it
                if (setBright < 0 || setBright > 100) return;

                console.warn(`Sunrise ${lamp.dim.name} -> ${setBright} (${overallProgress.toFixed(3)})`);
                lamp.sw.sendCommand('ON');
                lamp.dim.sendCommand(setBright);
            });

            // Update CT (in reverse, 100 warm -> 0 cold) on lamps having a CT item
            const ctProgress = Math.max(0, (overallProgress - CT_START_PROGRESS) / (1 - CT_START_PROGRESS));
            const ctValue = Math.round(100 - ctProgress * 100);

            if (ctValue !== lastCt) {
                lastCt = ctValue;
                lamps.filter((lamp) => lamp.ct).forEach((lamp) => lamp.ct.sendCommand(ctValue));
            }

            if (overallProgress >= 1) {
                console.warn('Sunrise emulation done');
                return;
            }

            sunriseTimer = setTimeout(() => tick(brightness + BRIGHT_STEP_PERCENT, true), tickMs);
        };

        tick(0, false);
    },
});
