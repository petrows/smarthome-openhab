#!/usr/bin/env python3

# # Devices, used in this configuration
class DEVICES:
    # IKEA Lamps
    IKEA_TRADFRI_LAMP_CLEAR_806 = {
        'types': [
            'zigbee',
            'lamp',
            'ikea',
            'ct',
        ],
        'device_name': 'IKEA TRADFRI LED bulb E27 806 lumen, dimmable, white spectrum, clear (LED1736G9)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/LED1736G9.html',
    }
    IKEA_TRADFRI_LAMP_CT_1000 = {
        'types': [
            'zigbee',
            'lamp',
            'ikea',
            'ct',
        ],
        'device_name': 'IKEA TRADFRI LED bulb E27 1000 lumen, dimmable, white spectrum, opal white (LED1732G11)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/LED1732G11.html',
    }
    IKEA_TRADFRI_LAMP_W_806 = {
        'types': [
            'zigbee',
            'lamp',
            'ikea',
        ],
        'device_name': 'IKEA TRADFRI LED bulb E26/E27 806 lumen, dimmable, warm white (LED1836G9)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/LED1836G9.html',
    }
    IKEA_TRADFRI_LAMP_W_250 = {
        'types': [
            'zigbee',
            'lamp',
            'ikea',
        ],
        'device_name': 'IKEA TRADFRI LED bulb E27 WW clear 250 lumen, dimmable (LED1842G3)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/LED1842G3.html',
    }
    IKEA_TRADFRI_LAMP_COLOR_600 = {
        'types': [
            'zigbee',
            'lamp',
            'ikea',
            'color',
        ],
        'device_name': 'TRADFRI LED bulb E14/E26/E27 600 lumen, dimmable, color, opal white (ebay)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/LED1624G9.html',
    }
    # IKEA Motion
    IKEA_TRADFRI_MOTION_SENSOR = {
        'types': [
            'zigbee',
            'motion',
            'ikea',
            'activity',
            'battery',
        ],
        'device_name': 'IKEA TRADFRI motion sensor (E1525/E1745)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/E1525_E1745.html',
    }
    # IKEA Remotes
    # The possible values are: toggle, arrow_left_click, arrow_right_click, arrow_left_hold, arrow_right_hold, arrow_left_release, arrow_right_release, brightness_up_click, brightness_down_click, brightness_up_hold, brightness_up_release, brightness_down_release, toggle_hold
    IKEA_TRADFRI_REMOTE = {
        'types': [
            'zigbee',
            'remote',
            'ikea',
            'battery',
        ],
        'device_name': 'IKEA TRADFRI remote control (E1524/E1810)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/E1524_E1810.html',
    }
    # The possible values are: on, off, brightness_move_down, brightness_move_up, brightness_stop
    IKEA_TRADFRI_ON_OFF = {
        'types': [
            'zigbee',
            'remote',
            'ikea',
            'battery',
        ],
        'device_name': 'IKEA TRADFRI ON/OFF switch (E1743)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/E1743.html',
    }
    # The possible values are: on, off, brightness_move_up, brightness_move_down, brightness_stop, arrow_left_click, arrow_right_click, arrow_left_hold, arrow_right_hold, arrow_left_release, arrow_right_release
    IKEA_TRADFRI_STYRBAR = {
        'types': [
            'zigbee',
            'remote',
            'ikea',
            'battery',
        ],
        'device_name': 'IKEA STYRBAR remote control N2',
        'device_url': 'https://www.zigbee2mqtt.io/devices/E2001_E2002.html',
    }
    # Sockets
    OSRAM_SMART_PLUG = {
        'types': [
            'zigbee',
            'plug',
        ],
        'device_name': 'OSRAM Smart+ plug',
        'device_url': 'https://www.zigbee2mqtt.io/devices/AB3257001NJ.html',
    }
    # Xiaomi sensors
    XIAOMI_AQARA_V1 = {
        'types': [
            'zigbee',
            'temperature',
            'humidity',
            'activity',
            'battery',
            'voltage',
        ],
        'device_name': 'Xiaomi MiJia temperature & humidity sensor (WSDCGQ01LM)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/WSDCGQ01LM.html',
    }
    XIAOMI_AQARA_V2 = {
        'types': [
            'zigbee',
            'temperature',
            'humidity',
            'pressure',
            'activity',
            'battery',
            'voltage',
        ],
        'device_name': 'Xiaomi Aqara temperature, humidity and pressure sensor (WSDCGQ11LM)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/WSDCGQ11LM.html',
    }
    XIAOMI_AQARA_LEAK_V1 = {
        'types': [
            'zigbee',
            'leak',
            'activity',
            'battery',
            'voltage',
        ],
        'device_name': 'Xiaomi Aqara water leak sensor (SJCGQ11LM)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/SJCGQ11LM.html',
    }
    # The possible values are: single, double, tripple, quadruple, hold, release
    XIAOMI_BUTTON = {
        'types': [
            'zigbee',
            'remote',
            'battery',
            'voltage',
        ],
        'device_name': 'Xiaomi MiJia wireless switch (WXKG01LM)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/WXKG01LM.html',
    }
    # Aldi
    ALDI_FILAMENT = {
        'types': [
            'zigbee',
            'lamp',
            'aldi',
            'ct',
        ],
        'device_name': 'Aldi LIGHTWAY smart home LED-lamp - filament (F122SB62H22A4.5W)',
        'device_url': '?',
    }
    # Heiman
    HEIMAN_SW_1_GANG = {
        'types': [
            'zigbee',
            'plug',
            'heiman',
            'device_temperature',
        ],
        'device_name': 'HEIMAN Smart switch - 1 gang with neutral wire (HS2SW1A/HS2SW1A-N)',
        'device_url': 'https://zigbee.blakadder.com/Heiman_HS2SW1A.html',
    }
    # Tuya
    TUYA_THERMOSTAT_VALVE = {
        'types': [
            'zigbee',
            'thermostat',
            'temperature',
            'position',
            'activity',
            # 'battery_low', # For using akkus - invalid battery level reporting
        ],
        'device_name': 'TuYa Radiator valve with thermostat (TS0601_thermostat)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/TS0601_thermostat.html',
    }
    TUYA_WINDOW_SENSOR = {
        'types': [
            'zigbee',
            'contact',
            'battery',
            'voltage',
        ],
        'device_name': 'TuYa Rechargeable Zigbee contact sensor (SNTZ007)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/SNTZ007.html',
    }
    TUYA_TEMPERATURE_SENSOR_TS0201 = {
        'types': [
            'zigbee',
            'temperature',
            'humidity',
            'activity',
            'battery',
            'voltage',
        ],
        'device_name': 'TuYa Temperature & humidity sensor',
        'device_url': 'https://www.zigbee2mqtt.io/devices/TS0201.html',
    }
    TUYA_WALL_RELAY = {
        'types': [
            'zigbee',
            'contact',
            'battery',
            'voltage',
        ],
        'device_name': 'TuYa Wall switch module (WHD02)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/WHD02.html',
    }
    TUYA_WALL_SWITCH_TS0601 = {
        'types': [
            'zigbee',
            'plug_mt',
        ],
        'device_name': 'TS0601_switch - TuYa 1, 2, 3 or 4 gang switch (Router)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/TS0601_switch.html',
    }
    # Lidl smart home - Silvercrest
    SILVERCREST_SMART_PLUG = {
        'types': [
            'zigbee',
            'plug',
        ],
        'device_name': 'Lidl Silvercrest smart plug (EU, CH, FR, BS, DK) (HG06337)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/HG06337.html',
    }
    # DIY
    DIY_CC2540_ROUTER = {
        'types': [
            'zigbee',
        ],
        'device_name': 'CC2530.ROUTER - Custom devices (DiY)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/CC2530.ROUTER.html',
    }
    # Sonoff-tasmota
    TASMOTA_SONOFF_MINI = {
        'types': [
            'tasmota',
            'activity',
            'rssi',
            'bssid',
            'la',
        ],
        'device_name': 'Sonoff Mini Switch',
        'device_url': 'https://templates.blakadder.com/sonoff_mini.html',
        'tasmota_channels': [
            {
                'type': 'switch',
                'id': 'POWER',
            }
        ]
    }
    TASMOTA_SONOFF_TOUCH_EU1 = {
        'types': [
            'tasmota',
            'activity',
            'rssi',
            'bssid',
            'la',
        ],
        'device_name': 'Sonoff Touch EU Switch (1 gang)',
        'device_url': 'https://templates.blakadder.com/sonoff_touch_eu.html',
        'tasmota_channels': [
            {
                'type': 'switch',
                'id': 'POWER',
            }
        ]
    }
    TASMOTA_SONOFF_TOUCH_EU2 = {
        'types': [
            'tasmota',
            'activity',
            'rssi',
            'bssid',
            'la',
        ],
        'device_name': 'Sonoff Touch EU Switch (2 gang)',
        'device_url': 'https://templates.blakadder.com/sonoff_touch_eu.html',
        'tasmota_channels': [
            {
                'type': 'switch',
                'id': 'POWER1',
            },
            {
                'type': 'switch',
                'id': 'POWER2',
            }
        ]
    }
    SILVERCREST_THERMOSTAT_368308_2010 = {
        'types': [
            'zigbee',
            'thermostat',
            'temperature',
            'activity',
            'voltage',
            'battery_voltage',
        ],
        'batt_type': '1xAA', # Device reports value seems to be 'per element' (it has 2xAA)
        'device_name': 'Silvercrest radiator valve with thermostat',
        'device_url': 'https://www.zigbee2mqtt.io/devices/368308_2010.html',
    }
