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


Sensor({
    id: 'ku_climate',
    name: 'Климат',
    room: ROOMS.KITCHEN,
}),

]
}
