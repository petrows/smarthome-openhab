/*

Config for Yandex2mqtt bridge

To expose devices to Yandex Smart Home and Alice smart station.

Config for PWS fork: https://github.com/petrows/yandex2mqtt

*/

// Preambula: define helpers, to avoid duplicating

const tpl = require('./yandex2mqtt.template')

const { LIGHT, Light, Thermostat, Sensor, Shutter } = tpl

const ROOMS = {
    LOBBY: 'Прихожая',
    WC: 'Ванная',
    SLEEP: 'Спальня',
    KITCHEN: 'Кухня',
    LIVING: 'Гостиная',
    KG_CABINET: 'Кабинет',
}

module.exports = {
    devices: [
        // Corridor
        Light(LIGHT.DIM, {
            id: 'fl_up_light',
            name: 'Верхний',
            room: ROOMS.LOBBY,
        }),
        Light(LIGHT.DIM, {
            id: 'eg_decoration_light',
            name: 'Комод',
            room: ROOMS.LOBBY,
        }),

        // WC
        Light(LIGHT.CT, {
            id: 'bz_light_1',
            name: 'Верхний туалет',
            room: ROOMS.WC,
            proxy: true,
        }),
        Light(LIGHT.CT, {
            id: 'bz_light_2',
            name: 'Верхний душ',
            room: ROOMS.WC,
            proxy: true,
        }),
        Light(LIGHT.SW, {
            id: 'bz_mirror',
            name: 'Зеркало',
            room: ROOMS.WC,
        }),

        // Sleeproom
        Light(LIGHT.CT, {
            id: 'sz_up_light',
            name: 'Верхний',
            room: ROOMS.SLEEP,
        }),
        Light(LIGHT.CT, {
            id: 'sz_bed_light',
            name: 'Кровать',
            room: ROOMS.SLEEP,
        }),

        Thermostat({
            id: 'sz_heating',
            name: 'Отопление',
            room: ROOMS.SLEEP,
        }),
        Sensor({
            id: 'sz_climate',
            name: 'Климат',
            room: ROOMS.SLEEP,
        }),
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

        // Kitchen
        Shutter({
            id: 'ku_blinds',
            name: 'Жалюзи',
            room: ROOMS.KITCHEN,
        }),

        // Зал
        Shutter({
            id: 'wz_blinds',
            name: 'Жалюзи',
            room: ROOMS.LIVING,
        }),

        // KG (Cabinet)
        Light(LIGHT.CT, {
            id: 'desktop_petro_light',
            name: 'Стол',
            room: ROOMS.KG_CABINET,
        }),
        Thermostat({
            id: 'kg_heating',
            name: 'Отопление',
            room: ROOMS.KG_CABINET,
        }),
        Sensor({
            id: 'kg_climate',
            name: 'Климат',
            room: ROOMS.KG_CABINET,
        }),
    ],
};
