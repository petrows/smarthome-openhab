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
    # IKEA Motion
    IKEA_TRADFRI_MOTION_SENSOR = {
        'types': [
            'zigbee',
            'motion',
            'ikea',
            'battery',
        ],
        'device_name': 'IKEA TRADFRI motion sensor (E1525/E1745)',
        'device_url': 'https://www.zigbee2mqtt.io/devices/E1525_E1745.html',
    }
    # IKEA Remotes
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
    # Sockets
    OSRAM_SMART_PLUG = {
        'types': [
            'zigbee',
            'plug',
        ],
        'device_name': 'OSRAM Smart+ plug',
        'device_url': 'https://www.zigbee2mqtt.io/devices/AB3257001NJ.html',
    }
