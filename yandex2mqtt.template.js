/*
    Yandex2mqtt template classes

    Used by codegen updated on each Codegen call!
*/

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

// Common object to represent custom program
function Scene(options) {
    if (!options.type) { options.type = 'devices.types.switch' }
    let dev = new GenDevice(options)
    // Scene can ON/OFF
    dev.addMQTT('on', options.id + '/sw', options.id)
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
        state: {
            instance: 'on',
            value: false,
        },
    })
    return dev.toConfig()
}

const LIGHT = {
    SW: 'sw', // Simple, on/off
    DIM: 'dim', // on/off, dimmer
    CT: 'ct', // on/off, dimmer, Color temperature
    RGB: 'rgb', // on/off, dimmer, RGB
}

function LightGroup(options) {
    if (!options.type) { options.type = 'devices.types.light' }
    let dev = new GenDevice(options)
    // Group lights can ON/OFF
    dev.addMQTT('on', options.id + '/sw', options.id)
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
        state: {
            instance: 'on',
            value: false,
        },
    })
    return dev.toConfig()
}

function Light(type, options) {
    if (!options.type) { options.type = 'devices.types.light' }
    if (typeof options.sw === 'undefined') { options.sw = '_sw' }
    let dev = new GenDevice(options)
    // Special suffux for buggy devices (use not real item, but proxy)
    let suffix = options.proxy ? '_proxy' : ''
    // All lights can ON/OFF
    dev.addMQTT('on', options.id + options.sw + suffix + '/sw', options.id + options.sw + suffix)
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
    // Device settings
    options.temp_off = options.temp_off || 5
    options.temp_on = options.temp_on || 20
    options.temp_on_min = options.temp_on_min || 15
    let dev = new GenDevice(options)
    // On/Off control
    dev.addMQTT('on', options.id + '_thermostat/temperature', options.id + '_thermostat')
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
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
    })
    // Конвертация, для эмуляции ВКЛ/ВЫКЛ отопления
    dev.addValueMapping({
        type: 'on_off',
        mapping: function (device, instance, value, y2m) {
            // Кастомная функция конвертации
            if (y2m) { // От Яндекс в MQTT
                return value ? options.temp_on : options.temp_off
            } else { // От MQTT в Яндекс
                // Если температура больше 17°C -> репортим ВКЛ, иначе ВЫКЛ
                return value > options.temp_on_min
            }
        }
    })
    return dev.toConfig()
}

function SensorClimate(options) {
    if (!options.type) { options.type = 'devices.types.sensor.climate' }
    let dev = new GenDevice(options)
    // Special suffux for signle / group devices
    let suffix = options.proxy ? '_proxy' : ''
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
    dev.addValueMapping({
        type: 'float',
        mapping: function (device, instance, value, y2m) {
            if ('humidity' == instance) {
                // Convert humidity from 0-1.0 to 0-100%
                return Math.round(value * 100.0)
            }
            if ('pressure' == instance) {
                // Convert hPa to atm
                return (parseFloat(value) * 0.750062)
            }
            if ('co2_level' == instance) {
                // Convert CO2 from 1/1M to ppm
                return Math.round(value * 1000000.0)
            }
            return value
        }
    })
    if (options.co2) {
        dev.addMQTT('co2_level', null, options.id + '_co2')
        dev.addProperty({
            type: 'devices.properties.float',
            retrievable: true,
            reportable: true,
            parameters: {
                instance: 'co2_level',
                unit: 'unit.ppm',
            },
            state: {
                instance: 'co2_level',
                value: 0,
            },
        })
    }
    if (options.pressure) {
        dev.addMQTT('pressure', null, options.id + '_pressure')
        dev.addProperty({
            type: 'devices.properties.float',
            retrievable: true,
            reportable: true,
            parameters: {
                instance: 'pressure',
                unit: 'unit.pressure.mmhg',
            },
            state: {
                instance: 'pressure',
                value: 0,
            },
        })
    }
    return dev.toConfig()
}

function SensorWindow(options) {
    if (!options.type) { options.type = 'devices.types.sensor.open' }
    let dev = new GenDevice(options)
    dev.addMQTT('open', null, options.id + '_contact')
    dev.addProperty({
        type: 'devices.properties.event',
        retrievable: true,
        reportable: true,
        parameters: {
            instance: 'open',
            events: [
                { 'value': 'opened' },
                { 'value': 'closed' },
            ]
        },
        state: {
            instance: 'open',
            value: 'opened',
        },
    })
    // Conversion for Yandex states from OpenHAB:
    // OPEN -> opened, CLOSED -> closed
    dev.addValueMapping({
        type: 'event',
        mapping: function (device, instance, value, y2m) {
            value = value.toLowerCase()
            if (value == 'open') return 'opened'
            if (value == 'false') return 'opened'
            if (value == 'close') return 'closed'
            if (value == 'true') return 'closed'
            return value
        }
    })
    return dev.toConfig()
}

// Жалюзи твёрдые
function Shutter(options) {
    if (!options.type) { options.type = 'devices.types.openable.curtain' }
    let dev = new GenDevice(options)

    // Открой-закрой (конвертация функцией)
    dev.addMQTT('on', options.id + '_pos/pos', options.id + '_pos')
    dev.addCapability({
        type: 'devices.capabilities.on_off',
        retrievable: true,
        reportable: true,
    })
    // Вычисление и усправление ON/OFF -> открой / закрой
    dev.addValueMapping({
        type: 'on_off',
        mapping: function (device, instance, value, y2m) {
            // Кастомная функция конвертации
            // У меня % означают "насколько закрыто"
            if (y2m) { // От Яндекс в MQTT
                return value ? 0 : 100
            } else { // От MQTT в Яндекс
                // Закрыто менее чем на 90% -> открыто
                return value < 90
            }
        }
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
    Scene: Scene,
    LightGroup: LightGroup,
    Light: Light,
    Thermostat: Thermostat,
    SensorClimate: SensorClimate,
    SensorWindow: SensorWindow,
    Shutter: Shutter,
}
