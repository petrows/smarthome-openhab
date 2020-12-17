#!/usr/bin/env python3
"""
    This script provides OpenHab codegen functionality.
    Purpose: generate repeating items config.

    Plug - have only ON/OFF states
"""

import os
import logging
import argparse
import numpy as np

logging.basicConfig(level=logging.DEBUG)

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class DEVICES:
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
    OSRAM_SMART_PLUG = {
        'types': [
            'zigbee',
            'plug',
        ],
        'device_name': 'OSRAM Smart+ plug',
        'device_url': 'https://www.zigbee2mqtt.io/devices/AB3257001NJ.html',
    }


items = [
    # {
    #     'name': "Petro Desktop",
    #     'id': "light_desktop_petro",
    #     'zigbee_id': '0xccccccfffed8ef9d',
    #     'type': DEVICES.IKEA_TRADFRI_LAMP_CLEAR_806,
    # },
    {
        'name': "Petro Desktop power",
        'id': "desktop_petro_power",
        'zigbee_id': '0x7cb03eaa0a094bf2',
        'type': DEVICES.OSRAM_SMART_PLUG,
    },
]


def device_comment(item):
    device_id = ''
    if np.in1d(['zigbee'], item['type']['types']).any():
        device_id = item['zigbee_id']
    conf_str = []
    conf_str.append(f"// {item['name']} ({device_id})")
    conf_str.append(
        f"// {item['type']['device_name']}"
        f" / {item['type']['device_url']}"
    )
    return conf_str


def device_short_id(id):
    return id[-4:]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Openhab codegen')

    parser.add_argument(
        '--write', action='store_true', help='Write config files to FS')

    args = parser.parse_args()

    # Generate some common values
    zigbee_ids = []
    for x, item in enumerate(items):
        if np.in1d(['zigbee'], item['type']['types']).any():
            # Add to all Zigbee items generated MQTT topic like "zigbee-XXXX"
            items[x]['zigbee_short'] = device_short_id(item['zigbee_id'])
            items[x]['mqtt_topic'] = f"zigbee-{items[x]['zigbee_short']}"
            # Add ids to check conflicts
            if items[x]['zigbee_short'] in zigbee_ids:
                raise Exception("Device ID is not unique!")
            zigbee_ids.append(items[x]['zigbee_short'])

    # Generate THINGS
    conf_str = []
    for item in items:
        # Zigbee2mqtt device?
        if 'zigbee' in item['type']['types']:
            conf_str.extend(device_comment(item))
            conf_str.append(
                f"Thing mqtt:topic:openhab:{item['mqtt_topic']} (mqtt:broker:openhab) {{")
            conf_str.append(
                f"\tChannels:")
            # Device have switch option
            if np.in1d(['lamp', 'plug'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : state [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\", transformationPattern=\"JSONPATH:$.state\", transformationPatternOut=\"JS:z2m-command-state.js\"]")

            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"\t\tType number : link [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.linkquality\"]")
            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"\t\tType switch : ota [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JS:z2m-ota.js\"]")
            conf_str.append(
                f"}}")

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'things', 'gen.things'), 'w')
        f.write(conf_str)
        f.close()

    # Generate ITEMS
    conf_str = []
    for item in items:
        logging.info(f"Processing device {item['name']}")
        conf_str.extend(device_comment(item))
        # Some devices have switch option
        if np.in1d(['lamp', 'plug'], item['type']['types']).any():
            device_icon = 'power'
            if 'lamp' in item['type']['types']:
                device_icon = 'light'
            conf_str.append(
                f"Switch {item['id']}_sw \"{item['name']}\""
                f" <{device_icon}> {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:state\"}}"
            )
        if np.in1d(['zigbee'], item['type']['types']).any():
            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"Number {item['id']}_link \"{item['name']} [%d %%]\""
                f" <network> (g_zigbee_link) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:link\"}}"
            )
            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"Switch {item['id']}_ota \"{item['name']} [%s]\""
                f" <settings> (g_zigbee_ota) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ota\"}}"
            )
            # Some zigbee devices report battery
            if 'battery' in item['type']['types']:
                conf_str.append(
                    f"Switch {item['id']}_battery_low \"{item['name']} [MAP(lowbat.map):%s]\""
                    f" <lowbattery> (g_battery_low) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery_low\"}}"
                )

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'items', 'gen.items'), 'w')
        f.write(conf_str)
        f.close()
