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
    OSRAM_SMART_PLUG = {
        'types': [
            'zigbee',
            'plug',
        ],
        'device_name': 'OSRAM Smart+ plug',
        'device_url': 'https://www.zigbee2mqtt.io/devices/AB3257001NJ.html',
    }


items = [
    # EG (Foto Studio)
    {
        'name': "Marina Desktop light",
        'id': "desktop_marina_light",
        'zigbee_id': '0xec1bbdfffe1b89d1',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_fs'],
            'ct': ['g_light_astro_color'],
        }
    },
    # KG
    {
        'name': "Petro Desktop light",
        'id': "desktop_petro_light",
        'zigbee_id': '0xccccccfffed8ef9d',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CLEAR_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg'],
            'ct': ['g_light_astro_color'],
        }
    },
    {
        'name': "Petro Desktop power",
        'id': "desktop_petro_power",
        'zigbee_id': '0x7cb03eaa0a094bf2',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_kg_power'],
        }
    },
    {
        'name': "KG Lager 4 (1)",
        'id': "kg_lager4_1_light",
        'zigbee_id': '0xccccccfffedf345a',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_auto', 'g_light_lager_auto'],
            'dim': ['g_dim_lager_auto'],
        }
    },
    {
        'name': "KG Lager 4 (2)",
        'id': "kg_lager4_2_light",
        'zigbee_id': '0xccccccfffedf5314',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_auto', 'g_light_lager_auto'],
            'dim': ['g_dim_lager_auto'],
        }
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


def device_groups(item, typ):
    if typ in item['groups']:
        return ' (' + ','.join(item['groups'][typ])+')'
    return ''


def device_short_id(id):
    return id[-4:]


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Openhab codegen')

    parser.add_argument(
        '--write', action='store_true', help='Write config files to FS')

    args = parser.parse_args()

    logging.info(f"Processing {len(items)} devices")

    # Generate some common values
    zigbee_ids = []
    for x, item in enumerate(items):
        if np.in1d(['zigbee'], item['type']['types']).any():
            # Add to all Zigbee items generated MQTT topic like "zigbee-XXXX"
            items[x]['zigbee_short'] = device_short_id(item['zigbee_id'])
            items[x]['mqtt_topic'] = f"{items[x]['id']}"
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
                    f"\t\tType switch : state ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.state\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-state.js\""
                    f"]"
                )
            # Device have dimmer
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : dim ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.brightness\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-brightness.js\", min=1, max=255"
                    f"]"
                )
            # Device have Colot Temp control
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : ct ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.color_temp\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-color_temp.js\", min=150, max=500"
                    f"]"
                )

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
    all_items = []
    gen_rules = []  # Special rules for devices
    for item in items:
        conf_str.extend(device_comment(item))
        # Some devices have switch option
        if np.in1d(['lamp', 'plug'], item['type']['types']).any():
            device_icon = 'switch'
            if 'lamp' in item['type']['types']:
                device_icon = 'light'
            conf_str.append(
                f"Switch {item['id']}_sw \"{item['name']}\" <{device_icon}>"
                f"{device_groups(item,'sw')}"
                f"{{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:state\"}}"
            )
            all_items.append(f"Switch item={item['id']}_sw")

        if np.in1d(['zigbee'], item['type']['types']).any():
            # All Zigbee lamps have dimmer built-in
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_dim \"{item['name']} DIM [%d %%]\"  <{device_icon}>"
                    f"{device_groups(item,'dim')}"
                    f"{{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:dim\"}}"
                )
                all_items.append(f"Slider item={item['id']}_dim")

            # Zigbee color temperature
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_ct \"{item['name']} CT [JS(display-mired.js):%s]\" <{device_icon}>"
                    f"{device_groups(item,'ct')}"
                    f"{{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ct\"}}"
                )
                all_items.append(f"Slider item={item['id']}_ct")
                gen_rules.append(
                    f"""
# Device should apply saved color temp when ON
rule "{item['name']} apply color on ON"
when
    Item {item['id']}_sw changed to ON
then
	{item['id']}_ct.sendCommand({item['id']}_ct.state)
end
"""
                )

            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"Number {item['id']}_link \"{item['name']} [%d]\""
                f" <network> (g_zigbee_link) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:link\"}}"
            )
            # all_items.append(f"Text item={item['id']}_link")

            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"Switch {item['id']}_ota \"{item['name']} [%s]\""
                f" <flowpipe> (g_zigbee_ota) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ota\"}}"
            )
            # all_items.append(f"Switch item={item['id']}_ota")

            # Some zigbee devices report battery
            if 'battery' in item['type']['types']:
                conf_str.append(
                    f"Switch {item['id']}_battery_low \"{item['name']} [MAP(lowbat.map):%s]\""
                    f" <lowbattery> (g_battery_low) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery_low\"}}"
                )
                # all_items.append(f"Switch item={item['id']}_battery_low")

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'items', 'gen.items'), 'w')
        f.write(conf_str)
        f.close()

    # Write test sitemap
    test_sitemap = """
sitemap gen label="GEN ITEMS"
{
    Frame {
        """ + "\n        ".join(all_items) + """
    }
}
    """
    print(test_sitemap)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'sitemaps', 'gen.sitemap'), 'w')
        f.write(test_sitemap)
        f.close()

    # Write generated rules
    gen_rules = '\n'.join(gen_rules)
    print(gen_rules)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'rules', 'gen.rules'), 'w')
        f.write(gen_rules)
        f.close()
