/*

Config for Yandex2mqtt bridge

To expose devices to Yandex Smart Home and Alice smart station.

Config for PWS fork: https://github.com/petrows/yandex2mqtt

*/

// Preambula: define helpers, to avoid duplicating

const tpl = require('./yandex2mqtt.template')
const cdg = require('./yandex2mqtt.codegen')

const { LIGHT, Scene, LightGroup, Light, Thermostat, SensorClimate, SensorWindow, Shutter } = tpl

const ROOMS = {
    GROUPS: 'Группы',
    LOBBY: 'Коридор (прихожая)',
    WC: 'Ванная',
    SLEEP: 'Спальня',
    KITCHEN: 'Кухня',
    LIVING: 'Гостиная',
    KINO: 'Кинозал',
    KG_CABINET: 'Кабинет',
    BALKON: 'Балкон',
}

devices = [
    // Scenes
    Scene({
        id: 'scene_sleep',
        name: 'Хочу спать',
        room: ROOMS.GROUPS,
    }),
    Scene({
        id: 'scene_cat_food',
        name: 'Покорми котов',
        room: ROOMS.GROUPS,
    }),

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
    Light(LIGHT.CT, {
        id: 'bk_up_light',
        name: 'Верхний',
        room: ROOMS.BALKON,
    }),

    // Window sensors group
    SensorWindow({
        id: 'ku_windows',
        name: 'Окна',
        room: ROOMS.KITCHEN,
    }),
    SensorWindow({
        id: 'sz_windows',
        name: 'Окна',
        room: ROOMS.SLEEP,
    }),
    SensorWindow({
        id: 'ks_windows',
        name: 'Окна',
        room: ROOMS.KINO,
    }),
    SensorWindow({
        id: 'wz_windows',
        name: 'Окна',
        room: ROOMS.LIVING,
    }),
    SensorWindow({
        id: 'kg_windows',
        name: 'Окна',
        room: ROOMS.KG_CABINET,
    }),
    SensorWindow({
        id: 'bz_windows',
        name: 'Окна',
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

    // Christmas lights
    Light(LIGHT.SW, {
        id: 'sz_christmas_light',
        type: 'devices.types.switch',
        name: 'Гирлянда',
        room: ROOMS.SLEEP,
    }),
    Light(LIGHT.SW, {
        id: 'ks_christmas_light',
        type: 'devices.types.switch',
        name: 'Гирлянда',
        room: ROOMS.KINO,
    }),
    Light(LIGHT.SW, {
        id: 'wz_christmas_light',
        type: 'devices.types.switch',
        name: 'Гирлянда',
        room: ROOMS.LIVING,
    }),
    Light(LIGHT.SW, {
        id: 'kg_christmas_light',
        type: 'devices.types.switch',
        name: 'Гирлянда',
        room: ROOMS.KG_CABINET,
    }),
    Light(LIGHT.SW, {
        id: 'bk_christmas_light',
        type: 'devices.types.switch',
        name: 'Гирлянда',
        room: ROOMS.BALKON,
    }),

    // Heater in BZ
    Light(LIGHT.SW, {
        id: 'bz_towel_heater',
        type: 'devices.types.switch',
        name: 'Полотенцесушитель',
        room: ROOMS.WC,
    }),

    // Plant lamp switch
    Light(LIGHT.SW, {
        id: 'wz_plant_light',
        type: 'devices.types.switch',
        name: 'Цветы',
        room: ROOMS.LIVING,
    }),
];

devices = devices.concat(cdg.devices)

module.exports = {
    devices: devices,
};
