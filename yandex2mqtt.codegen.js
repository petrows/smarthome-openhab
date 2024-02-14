const tpl = require("./yandex2mqtt.template")
const { LIGHT, LightGroup, Light, Thermostat, Sensor, Shutter } = tpl
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
  KG_CABINET: 'Кабинет',
  KG_BOILER: 'Котельная',
  KG_L1: 'Кладовка 1',
  KG_L4: 'Кладовка 4',
  KG_LAUNDRY: 'Прачечная',
}
module.exports = {
devices: [
Sensor({
    id: 'ext_climate',
    name: 'Климат',
    room: ROOMS.OUTSIDE,
}),
Light(LIGHT.CT, {
    id: 'bk_light_1',
    name: 'Верхний',
    room: ROOMS.BALKON,
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
Light(LIGHT.CT, {
    id: 'ks_up_light',
    name: 'Верхний',
    room: ROOMS.KINO,
}),
Sensor({
    id: 'ks_climate',
    name: 'Климат',
    room: ROOMS.KINO,
}),
Light(LIGHT.RGB, {
    id: 'ks_light_night',
    name: 'Декоративный',
    room: ROOMS.KINO,
}),
Sensor({
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
Light(LIGHT.DIM, {
    id: 'wz_declamp_1',
    name: 'Декор 1',
    room: ROOMS.LIVING,
}),
Light(LIGHT.DIM, {
    id: 'wz_declamp_2',
    name: 'Декор 2',
    room: ROOMS.LIVING,
}),
Light(LIGHT.DIM, {
    id: 'wz_declamp_3',
    name: 'Декор 3',
    room: ROOMS.LIVING,
}),
Sensor({
    id: 'sz_climate',
    name: 'Климат',
    room: ROOMS.SLEEP,
}),
Light(LIGHT.CT, {
    id: 'sz_up_light',
    name: 'Верхний',
    room: ROOMS.SLEEP,
}),
Light(LIGHT.CT, {
    id: 'sz_bed_light_l',
    name: 'Кровать левый',
    room: ROOMS.SLEEP,
}),
Light(LIGHT.CT, {
    id: 'sz_bed_light_r',
    name: 'Кровать правый',
    room: ROOMS.SLEEP,
}),
Sensor({
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
Sensor({
    id: 'tr_climate',
    name: 'Климат',
    room: ROOMS.TREPPE,
}),
Sensor({
    id: 'kg_climate',
    name: 'Климат',
    room: ROOMS.KG_CABINET,
}),
Light(LIGHT.CT, {
    id: 'desktop_petro_light',
    name: 'Стол',
    room: ROOMS.KG_CABINET,
}),
Sensor({
    id: 'lg3_climate',
    name: 'Климат',
    room: ROOMS.KG_LAUNDRY,
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
