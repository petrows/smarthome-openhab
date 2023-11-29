/*

Config for Yandex2mqtt bridge

To expose devices to Yandex Smart Home and Alice smart station.

Config for PWS fork: https://github.com/petrows/yandex2mqtt

*/

// Preambula: define helpers, to avoid duplicating

class GenDevice {
    data = {}
    constructor(options) {
        this.data = {}
        this.data.id = options.id
        this.data.type = options.type
        this.data.name = options.name || 'Без названия'
        this.data.description = options.description || ''
        this.data.room = options.room || ''
        this.data.mqtt = []
        this.data.capabilities = []
    }

    toConfig() {
        return this.data
    }

    addMQTT(instance, set, state) {
        this.data.mqtt.push({
            instance: instance,
            set: 'eventbus/set/' + set,
            state: 'eventbus/state/' + state,
        })
    }
    addCapability(cap) {
        this.data.capabilities.push(cap)
    }
}

const LIGHT = {
    SW: 'sw', // Simple, on/off
    DIM: 'dim', // on/off, dimmer
    CT: 'ct', // on/off, dimmer, Color temperature
    RGB: 'rgb', // on/off, dimmer, RGB
}

function Light(type, options) {
    if (!options.type) { options.type = 'devices.types.light' }
    let dev = new GenDevice(options)
    // Special suffux for buggy devices (use not real item, but proxy)
    let suffix = options.proxy ? '_proxy' : ''
    // All lights can ON/OFF
    dev.addMQTT('on', options.id + '_sw' + suffix + '/sw', options.id + '_sw' + suffix)
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
        state: {
            instance: 'on',
            value: false,
        },
    })
    // Device can DIM?
    if ([LIGHT.DIM, LIGHT.CT, LIGHT.RGB].includes(type)) {
        dev.addMQTT('brightness', options.id + '_dim/dim', options.id + '_dim')
        dev.addCapability({
            type: 'devices.capabilities.range',
            retrievable: true,
            reportable: true,
            parameters: {
                instance: 'brightness',
                unit: 'unit.percent',
                range: {
                    min: 1,
                    max: 100,
                    precision: 10
                }
            },
            state: {
                instance: 'brightness',
                value: 0,
            },
        })
    }
    // Device can CT?
    if ([LIGHT.CT].includes(type)) {
        dev.addMQTT('temperature_k', options.id + '_ct/ct_k', options.id + '_ct/ct_k')
        dev.addCapability({
            type: 'devices.capabilities.color_setting',
            retrievable: true,
            reportable: true,
            parameters: {
                instance: 'temperature_k',
                temperature_k: {
                    min: 2500,
                    max: 4000,
                }
            },
            state: {
                instance: 'temperature_k',
                value: 2500,
            },
        })
    }
    // Device can RGB?
    if ([LIGHT.RGB].includes(type)) {
        dev.addMQTT('rgb', options.id + '_color/rgb_int', null)
        dev.addCapability({
            type: 'devices.capabilities.color_setting',
            retrievable: true,
            reportable: true,
            parameters: {
                color_model: 'rgb',
            },
            state: {
                instance: 'rgb',
                value: 0,
            },
        })
    }
    return dev.toConfig()
}

const ROOMS = {
    LOBBY: 'Прихожая',
    WC: 'Ванная',
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
        // KG (Cabinet)
        Light(LIGHT.CT, {
            id: 'desktop_petro_light',
            name: 'Стол',
            room: ROOMS.KG_CABINET,
        }),
    ],
};
