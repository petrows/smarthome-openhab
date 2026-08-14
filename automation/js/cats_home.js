/**
 * @file Cats presence aggregator.
 *
 * Whenever a cat's AirTag "seen" status updates, rebuilds the list of cats
 * currently at home (those whose `at_<key>_location_seen` is "now") and writes
 * the comma-separated list of names to `at_cats_home` ("-" when nobody home).
 */

const { rules, triggers, items } = require('openhab');

/** Value of `at_<key>_location_seen` meaning the cat was just seen at home. */
const SEEN_NOW = 'now';

/** Cats: item name prefix -> display name. */
const CATS = [
    { key: 'mira', name: 'Мирочка' },
    { key: 'kst', name: 'Кшиштик' },
];

rules.JSRule({
    name: 'Cats at home',
    id: 'cats-at-home',
    triggers: CATS.map((cat) => triggers.ItemStateUpdateTrigger(`at_${cat.key}_location_seen`)),
    execute: () => {
        const atHome = CATS
            .filter((cat) => items.getItem(`at_${cat.key}_location_seen`).state === SEEN_NOW)
            .map((cat) => cat.name);

        items.getItem('at_cats_home').postUpdate(atHome.length > 0 ? atHome.join(', ') : '-');
    },
});
