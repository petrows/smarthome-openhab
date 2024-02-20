/*

Config for Yandex2mqtt bridge

To expose devices to Yandex Smart Home and Alice smart station.

Config for PWS fork: https://github.com/petrows/yandex2mqtt

*/

// Preambula: define helpers, to avoid duplicating

const tpl = require('./yandex2mqtt.template')
const cdg = require('./yandex2mqtt.codegen')

const { LIGHT, LightGroup, Light, Thermostat, Sensor, Shutter } = tpl

const ROOMS = {
    GROUPS: 'Группы',
    LOBBY: 'Коридор (прихожая)',
    WC: 'Ванная',
    SLEEP: 'Спальня',
    KITCHEN: 'Кухня',
    LIVING: 'Гостиная',
    KINO: 'Кинозал',
    KG_CABINET: 'Кабинет',
}

devices = [
    // Groups
    LightGroup({
        id: 'all_light',
        name: 'Все',
        room: ROOMS.GROUPS,
    }),
    LightGroup({
        id: 'eg_light',
        name: 'Верхний этаж',
        room: ROOMS.GROUPS,
    }),
    LightGroup({
        id: 'kg_light',
        name: 'Нижний этаж',
        room: ROOMS.GROUPS,
    }),
    Light(LIGHT.CT, {
        id: 'sz_bed_light',
        name: 'Кровать',
        room: ROOMS.SLEEP,
    }),
    Light(LIGHT.CT, {
        id: 'wz_light_decor',
        name: 'Декоративный',
        room: ROOMS.LIVING,
    }),
    Light(LIGHT.RGB, {
        id: 'bz_up_light',
        name: 'Верхний',
        room: ROOMS.WC,
    }),

    // Blinds
    Shutter({
        id: 'sz_blinds',
        name: 'Жалюзи',
        room: ROOMS.SLEEP,
    }),
    Shutter({
        id: 'sz_curtains',
        name: 'Шторы',
        room: ROOMS.SLEEP,
    }),
    Shutter({
        id: 'ku_blinds',
        name: 'Жалюзи',
        room: ROOMS.KITCHEN,
    }),

    Shutter({
        id: 'ks_blinds',
        name: 'Жалюзи',
        room: ROOMS.KINO,
    }),


    // Heating
    Thermostat({
        id: 'sz_heating',
        name: 'Отопление',
        room: ROOMS.SLEEP,
    }),
    Thermostat({
        id: 'ku_heating',
        name: 'Отопление',
        room: ROOMS.KITCHEN,
    }),
    Thermostat({
        id: 'ks_heating',
        name: 'Отопление',
        room: ROOMS.KINO,
    }),
    Thermostat({
        id: 'wz_heating',
        name: 'Отопление',
        room: ROOMS.LIVING,
    }),
    Thermostat({
        id: 'kg_heating',
        name: 'Отопление',
        room: ROOMS.KG_CABINET,
    }),
];

devices = devices.concat(cdg.devices)

module.exports = {
    devices: devices,
};
