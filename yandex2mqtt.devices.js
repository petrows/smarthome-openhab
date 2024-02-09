/*

Config for Yandex2mqtt bridge

To expose devices to Yandex Smart Home and Alice smart station.

Config for PWS fork: https://github.com/petrows/yandex2mqtt

*/

// Preambula: define helpers, to avoid duplicating

const tpl = require('./yandex2mqtt.template')

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

module.exports = {
    devices: [
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
            co2: true,
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
        Light(LIGHT.CT, {
            id: 'ku_up_light',
            name: 'Верхний',
            room: ROOMS.KITCHEN,
        }),
        Thermostat({
            id: 'ku_heating',
            name: 'Отопление',
            room: ROOMS.KITCHEN,
        }),
        Sensor({
            id: 'ku_climate',
            name: 'Климат',
            room: ROOMS.KITCHEN,
        }),
        Shutter({
            id: 'ku_blinds',
            name: 'Жалюзи',
            room: ROOMS.KITCHEN,
        }),

        // Кинозал
        Light(LIGHT.CT, {
            id: 'ks_up_light',
            name: 'Верхний',
            room: ROOMS.KINO,
        }),
        Light(LIGHT.RGB, {
            id: 'ks_light_night',
            name: 'Торшер',
            room: ROOMS.KINO,
        }),
        Shutter({
            id: 'ks_blinds',
            name: 'Жалюзи',
            room: ROOMS.KINO,
        }),
        Thermostat({
            id: 'ks_heating',
            name: 'Отопление',
            room: ROOMS.KINO,
        }),
        Sensor({
            id: 'ks_climate',
            name: 'Климат',
            room: ROOMS.KINO,
        }),

        // Зал
        Light(LIGHT.CT, {
            id: 'wz_up_light',
            name: 'Верхний',
            room: ROOMS.LIVING,
        }),
        Thermostat({
            id: 'wz_heating',
            name: 'Отопление',
            room: ROOMS.LIVING,
        }),
        Sensor({
            id: 'wz_climate',
            name: 'Климат',
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
