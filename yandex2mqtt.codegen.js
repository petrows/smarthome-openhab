const tpl = require("./yandex2mqtt.template")
const { LIGHT, LightGroup, Light, Thermostat, SensorClimate, SensorWindow, Shutter } = tpl
const ROOMS = {
  GROUPS: 'Группы',
  OUTSIDE: 'Улица',
  BALKON: 'Балкон',
  LOBBY: 'Коридор',
  WC: 'Ванная',
  SLEEP: 'Спальня',
  KITCHEN: 'Кухня',
  LIVING: 'Гостиная',
  KINO: 'Кинозал',
  TREPPE: 'Лестница',
  KG_WORKSHOP: 'Мастерская',
  KG_CABINET: 'Кабинет',
  KG_BOILER: 'Котельная',
  KG_L1: 'Кладовка 1',
  KG_L4: 'Кладовка 4',
  KG_LAUNDRY: 'Прачечная',
}
module.exports = {
devices: [
SensorClimate({
    id: 'ext_climate',
    name: 'Климат',
    room: ROOMS.OUTSIDE,
    pressure: true,
}),
Light(LIGHT.SW, {
    id: 'bk_color_light',
    name: 'Декоративный',
    room: ROOMS.BALKON,
    type: 'devices.types.switch',
}),
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
SensorWindow({
    id: 'eg_main_door',
    name: 'Входная дверь',
    room: ROOMS.LOBBY,
}),
Light(LIGHT.DIM, {
    id: 'fl_mirror',
    name: 'Зеркало',
    room: ROOMS.LOBBY,
}),
Light(LIGHT.RGB, {
    id: 'bz_light_1',
    name: 'Туалет',
    room: ROOMS.WC,
    proxy: true,
}),
Light(LIGHT.RGB, {
    id: 'bz_light_2',
    name: 'Душ',
    room: ROOMS.WC,
    proxy: true,
}),
Light(LIGHT.SW, {
    id: 'bz_mirror',
    name: 'Зеркало',
    room: ROOMS.WC,
    sw: '',
}),
Light(LIGHT.CT, {
    id: 'ks_up_light',
    name: 'Верхний',
    room: ROOMS.KINO,
}),
SensorClimate({
    id: 'ks_climate',
    name: 'Климат',
    room: ROOMS.KINO,
}),
Light(LIGHT.RGB, {
    id: 'ks_light_night',
    name: 'Декоративный',
    room: ROOMS.KINO,
}),
Light(LIGHT.SW, {
    id: 'ks_projector_power',
    name: 'Проектор',
    room: ROOMS.KINO,
    type: 'devices.types.switch',
}),
SensorClimate({
    id: 'wz_climate',
    name: 'Климат',
    room: ROOMS.LIVING,
}),
Light(LIGHT.CT, {
    id: 'wz_up_light',
    name: 'Верхний',
    room: ROOMS.LIVING,
}),
Light(LIGHT.RGB, {
    id: 'wz_julia_stand_light',
    name: 'Стол задник',
    room: ROOMS.LIVING,
}),
Light(LIGHT.CT, {
    id: 'wz_julia_desktop_light',
    name: 'Стол',
    room: ROOMS.LIVING,
}),
Light(LIGHT.RGB, {
    id: 'wz_light_color',
    name: 'Торшер',
    room: ROOMS.LIVING,
    proxy: true,
}),
SensorClimate({
    id: 'sz_climate',
    name: 'Климат',
    room: ROOMS.SLEEP,
    co2: true,
}),
Light(LIGHT.CT, {
    id: 'sz_up_light',
    name: 'Верхний',
    room: ROOMS.SLEEP,
}),
Light(LIGHT.RGB, {
    id: 'sz_bed_floor_light',
    name: 'Пол',
    room: ROOMS.SLEEP,
}),
Light(LIGHT.SW, {
    id: 'sz_tv_power',
    name: 'Телевизор',
    room: ROOMS.SLEEP,
    type: 'devices.types.switch',
}),
SensorClimate({
    id: 'ku_climate',
    name: 'Климат',
    room: ROOMS.KITCHEN,
}),
Light(LIGHT.DIM, {
    id: 'ku_light_table',
    name: 'Стол',
    room: ROOMS.KITCHEN,
}),
Light(LIGHT.SW, {
    id: 'ku_light_switch_haupt',
    name: 'Верхний',
    room: ROOMS.KITCHEN,
}),
Light(LIGHT.SW, {
    id: 'ku_light_switch_arbeit',
    name: 'Рабочий',
    room: ROOMS.KITCHEN,
}),
Light(LIGHT.CT, {
    id: 'tr_up_light',
    name: 'Верхний',
    room: ROOMS.TREPPE,
}),
Light(LIGHT.RGB, {
    id: 'tr_down_light',
    name: 'Нижний',
    room: ROOMS.TREPPE,
    proxy: true,
}),
SensorClimate({
    id: 'tr_climate',
    name: 'Климат',
    room: ROOMS.TREPPE,
}),
SensorClimate({
    id: 'kg_climate',
    name: 'Климат',
    room: ROOMS.KG_CABINET,
    co2: true,
    pressure: true,
}),
Light(LIGHT.CT, {
    id: 'desktop_petro_light',
    name: 'Стол',
    room: ROOMS.KG_CABINET,
}),
Light(LIGHT.SW, {
    id: 'kg_main1_work_light',
    name: 'Стол',
    room: ROOMS.KG_WORKSHOP,
}),
Light(LIGHT.SW, {
    id: 'kg_main1_light',
    name: 'Верхний',
    room: ROOMS.KG_WORKSHOP,
    sw: '',
}),
Light(LIGHT.SW, {
    id: 'kg_main2_light',
    name: 'Верхний',
    room: ROOMS.KG_CABINET,
    sw: '',
}),
Light(LIGHT.SW, {
    id: 'kg_hz_main_light',
    name: 'Верхний',
    room: ROOMS.KG_BOILER,
    sw: '',
}),
Light(LIGHT.SW, {
    id: 'kg_lager1_main_light',
    name: 'Верхний',
    room: ROOMS.KG_L1,
    sw: '',
}),
SensorClimate({
    id: 'lg3_climate',
    name: 'Климат',
    room: ROOMS.KG_LAUNDRY,
}),
Light(LIGHT.SW, {
    id: 'lg3_up_light',
    name: 'Верхний',
    room: ROOMS.KG_LAUNDRY,
    sw: '',
}),
Light(LIGHT.SW, {
    id: 'kg_lager4_main_light',
    name: 'Верхний',
    room: ROOMS.KG_L4,
    sw: '',
}),
Light(LIGHT.DIM, {
    id: 'kg_lager4_1_light',
    name: 'Дежурный 1',
    room: ROOMS.KG_L4,
}),
Light(LIGHT.DIM, {
    id: 'kg_lager4_2_light',
    name: 'Дежурный 2',
    room: ROOMS.KG_L4,
}),
]
}
