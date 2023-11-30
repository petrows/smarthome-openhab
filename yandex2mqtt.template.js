
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
        this.data.properties = []
        this.data.valueMapping = []
    }

    toConfig() {
        return this.data
    }

    addMQTT(instance, set, state) {
        //mqtt = {}
        //mqtt.instance =
        this.data.mqtt.push({
            instance: instance,
            ...(set ? {set: 'eventbus/set/' + set} : {} ),
            ...(state ? { state: 'eventbus/state/' + state } : {} ),
        })
    }
    addCapability(cap) {
        this.data.capabilities.push(cap)
    }
    addProperty(prop) {
        this.data.properties.push(prop)
    }
    addValueMapping(prop) {
        this.data.valueMapping.push(prop)
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
                value: 0,
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

function Thermostat(options) {
    if (!options.type) { options.type = 'devices.types.thermostat' }
    let dev = new GenDevice(options)
    // On/Off control
    dev.addMQTT('on', options.id + '_thermostat_enable', options.id + '_thermostat_enable')
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
        state: {
            instance: 'on',
            value: false,
        },
    })
    // Temperature control
    dev.addMQTT('temperature', options.id + '_thermostat/temperature', options.id + '_thermostat')
    dev.addCapability({
        type: 'devices.capabilities.range',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'temperature',
            unit: 'unit.temperature.celsius',
            range: {
                min: 5,
                max: 30,
                precision: 1
            }
        },
        state: {
            instance: 'temperature',
            value: 0,
        },
    })
    dev.addProperty({
        type: 'devices.properties.float',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'temperature',
            unit: 'unit.temperature.celsius',
        },
        state: {
            instance: 'temperature',
            value: 0,
        },
    })
    return dev.toConfig()
}

function Sensor(options) {
    if (!options.type) { options.type = 'devices.types.sensor.climate' }
    let dev = new GenDevice(options)
    // Temperature
    dev.addMQTT('temperature', null, options.id + '_temperature')
    dev.addMQTT('humidity', null, options.id + '_humidity')
    dev.addProperty({
        type: 'devices.properties.float',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'temperature',
            unit: 'unit.temperature.celsius',
        },
        state: {
            instance: 'temperature',
            value: 0,
        },
    })
    dev.addProperty({
        type: 'devices.properties.float',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'humidity',
            unit: 'unit.percent',
        },
        state: {
            instance: 'humidity',
            value: 0,
        },
    })
    return dev.toConfig()
}

// Жалюзи твёрдые
function Shutter(options) {
    if (!options.type) { options.type = 'devices.types.openable.curtain' }
    let dev = new GenDevice(options)

    // Открой-закрой
    dev.addMQTT('on', options.id + '_cmd/cmd', options.id + '_cmd')
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
        state: {
            instance: 'on',
            value: false,
        },
    })
    // Приведение к On -> open, Off -> close
    dev.addValueMapping({
        type: 'on_off',
        mapping: [[true, false], ["open", "close"]], // [yandex, mqtt]
    })

    // Положение
    dev.addMQTT('open', options.id + '_pos/pos', options.id + '_pos')
    dev.addCapability({
        type: 'devices.capabilities.range',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'open',
            unit: 'unit.percent',
            range: {
                min: 0,
                max: 100,
            }
        },
        state: {
            instance: 'open',
            value: 0,
        },
    })
    // Приведение к моему формату (0 - закрыто, 100 - открыто)
    dev.addValueMapping({
        type: 'range',
        mapping: 'invert_percent',
    })
    return dev.toConfig()
}

module.exports = {
    LIGHT: LIGHT,
    Light: Light,
    Thermostat: Thermostat,
    Sensor: Sensor,
    Shutter: Shutter,
}
