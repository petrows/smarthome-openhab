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

from codegen.devices import DEVICES

logging.basicConfig(level=logging.DEBUG)

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PREAMBULA = """
// ==========================================
// THIS FILE IS AUTO GENERATED
// Do not edit by hands
// Use this command to regenerate:
// python3 ./bin/codegen.py
// ==========================================

"""


# Items defentition
items = [
    # External (outside)
    {
        'name': "Outside Climate",
        'id': "ext_climate",
        'zigbee_id': '0x00158d0001c2cc22',
        'type': DEVICES.XIAOMI_AQARA_V1,
        'groups': {
            'sw': ['g_light_all'],
        }
    },
    {
        'name': "Balkon light 1",
        'id': "balkon_light_1",
        'zigbee_id': '0xec1bbdfffe4695b5',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_balkon'],
            'dim': ['g_dim_balkon'],
        }
    },
    # {
    #     'name': "Balkon light 2",
    #     'id': "balkon_light_2",
    #     'zigbee_id': '0xd0cf5efffee892b0',
    #     'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
    #     'groups': {
    #         'sw': ['g_light_all'],
    #         'ct': ['g_light_astro_color'],
    #     }
    # },
    # EG (Corridor)
    {
        'name': "Mirror remote",
        'id': "mirror_remote",
        'zigbee_id': '0x680ae2fffeab6b80',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "Leave switch",
        'id': "eg_leave_switch",
        'zigbee_id': '0x680ae2fffe16e111',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "EG Router",
        'id': "eg_router",
        'zigbee_id': '0x00124b000b4ed5cc',
        'type': DEVICES.DIY_CC2540_ROUTER,
    },
    # EG (Nagel Studio)
    {
        'name': "NS Climate",
        'id': "ns_climate",
        'zigbee_id': '0x00158d0001b95e08',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
    {
        'name': "NS Power 2",
        'id': "ns_power_2",
        'zigbee_id': '0x7cb03eaa0a093a8b',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'], # FIXME only for holidays!!!
        }
    },
    {
        'name': "NS Boost power",
        'id': "ns_boost_power",
        'zigbee_id': '0x7cb03eaa0a0a1103',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'expire': '1h'
    },
    {
        'name': "NS Projector",
        'id': "ns_projector_power",
        'zigbee_id': '0x7cb03eaa0a094d1d',
        'type': DEVICES.OSRAM_SMART_PLUG,
    },
    {
        'name': "NS Christmas light",
        'id': "ns_christmas_light",
        'zigbee_id': '0x7cb03eaa0a09e7bc',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'],
        }
    },
    # EG (Foto Studio)
    {
        'name': "FS Climate",
        'id': "fs_climate",
        'zigbee_id': '0x00158d0001c15121',
        'type': DEVICES.XIAOMI_AQARA_V1,
    },
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
    {
        'name': "Marina Desktop remote",
        'id': "desktop_marina_remote",
        'zigbee_id': '0xccccccfffeea9703',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "FS Christmas light",
        'id': "fs_christmas_light",
        'zigbee_id': '0x7cb03eaa0a09ad23',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'],
        }
    },
    # EG (Bedroom)
    {
        'name': "SZ Climate",
        'id': "sz_climate",
        'zigbee_id': '0x00158d0001c19a6b',
        'type': DEVICES.XIAOMI_AQARA_V1,
    },
    {
        'name': "Bedroom remote",
        'id': "sz_remote",
        'zigbee_id': '0x14b457fffe7e2305',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "SZ Decor lamp 1",
        'id': "sz_declamp_1",
        'zigbee_id': '0xec1bbdfffe972819',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_sz', 'g_light_eg_sz_night', 'g_light_eg_sz_decor'],
            'dim': ['g_light_eg_sz_night_brightness', 'g_light_eg_sz_decor_brightness'],
        }
    },
    {
        'name': "SZ Decor lamp 2",
        'id': "sz_declamp_2",
        'zigbee_id': '0xec1bbdfffe972203',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_sz', 'g_light_eg_sz_night', 'g_light_eg_sz_decor'],
            'dim': ['g_light_eg_sz_night_brightness', 'g_light_eg_sz_decor_brightness'],
        }
    },
    {
        'name': "SZ Decor lamp 3",
        'id': "sz_declamp_3",
        'zigbee_id': '0xec1bbdfffe91007b',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_sz', 'g_light_eg_sz_night', 'g_light_eg_sz_decor'],
            'dim': ['g_light_eg_sz_night_brightness', 'g_light_eg_sz_decor_brightness'],
        }
    },
    # EG (Kitchen)
    {
        'name': "KU Climate",
        'id': "ku_climate",
        'zigbee_id': '0x00158d0001b95fc4',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
    {
        'name': "KU Light Button",
        'id': "ku_light_button",
        'zigbee_id': '0x00158d0001be5b2d',
        'type': DEVICES.XIAOMI_BUTTON,
    },
    # Ladder (Treppe)
    {
        'name': "Treppe Up switch",
        'id': "treppe_up_switch",
        'zigbee_id': '0x680ae2fffe1a92f3',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "Treppe Down switch",
        'id': "treppe_down_switch",
        'zigbee_id': '0xccccccfffef0356e',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "Treppe Up light",
        'id': "treppe_up_light",
        'zigbee_id': '0xd0cf5efffee892b0',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'expire': '1h',
        'groups': {
            'sw': ['g_light_all', 'g_light_treppe', 'g_light_kg', 'g_light_kg_auto'],
            'dim': ['g_dim_treppe'],
            'ct': ['g_ct_treppe', 'g_light_astro_color'],
        }
    },
    {
        'name': "Treppe Down light",
        'id': "treppe_down_light",
        'zigbee_id': '0x588e81fffe507b40',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'expire': '1h',
        'groups': {
            'sw': ['g_light_all', 'g_light_treppe', 'g_light_kg', 'g_light_kg_auto'],
            'dim': ['g_dim_treppe'],
            'ct': ['g_ct_treppe', 'g_light_astro_color'],
        }
    },
    {
        'name': "Treppe motion",
        'id': "treppe_motion",
        'zigbee_id': '0xbc33acfffe872049',
        'type': DEVICES.IKEA_TRADFRI_MOTION_SENSOR,
    },
    # KG
    {
        'name': "KG Climate",
        'id': "kg_climate",
        'zigbee_id': '0x00158d0001b95e02',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
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
        'name': "Petro Desktop AUX",
        'id': "desktop_petro_aux_power",
        'zigbee_id': '0x7cb03eaa0a094bf2',
        'type': DEVICES.OSRAM_SMART_PLUG,
    },
    {
        'name': "Petro Desktop PC",
        'id': "desktop_petro_pc_power",
        'zigbee_id': '0x7cb03eaa0a094303',
        'type': DEVICES.OSRAM_SMART_PLUG,
    },
    {
        'name': "Petro Desktop remote",
        'id': "desktop_petro_remote",
        'zigbee_id': '0x000d6ffffee8357d',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "KG Lager 4 (1)",
        'id': "kg_lager4_1_light",
        'zigbee_id': '0xccccccfffedf345a',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'expire': '1h',
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_lager_auto'],
            'dim': ['g_dim_lager_auto'],
        }
    },
    {
        'name': "KG Lager 4 (2)",
        'id': "kg_lager4_2_light",
        'zigbee_id': '0xccccccfffedf5314',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'expire': '1h',
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_lager_auto'],
            'dim': ['g_dim_lager_auto'],
        }
    },
    {
        'name': "KG Lager switch",
        'id': "kg_lager4_switch",
        'zigbee_id': '0xccccccfffee401f8',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "KG Lager motion",
        'id': "kg_lager4_motion",
        'zigbee_id': '0xbc33acfffe84ca1e',
        'type': DEVICES.IKEA_TRADFRI_MOTION_SENSOR,
    },
    {
        'name': "KG Lager 4 leak",
        'id': "kg_lager4_leak",
        'zigbee_id': '0x00158d000488052c',
        'type': DEVICES.XIAOMI_AQARA_LEAK_V1,
    },
    # Heating
    {
        'name': "KG heating",
        'id': "kg_heating",
        'zigbee_id': '0x5c0272fffec9d557',
        'type': DEVICES.TUYA_THERMOSTAT_VALVE,
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
    if 'groups' in item and typ in item['groups']:
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
    item_ids = []
    zigbee_ids = []
    for x, item in enumerate(items):
        if item['id'] in item_ids:
            raise Exception(f"Device ID {item['id']} is not unique!")
        item_ids.append(item['id'])

        if np.in1d(['zigbee'], item['type']['types']).any():
            # Add to all Zigbee items generated MQTT topic like "zigbee-XXXX"
            items[x]['zigbee_short'] = device_short_id(item['zigbee_id'])
            items[x]['mqtt_topic'] = f"{items[x]['id']}"
            # Add ids to check conflicts
            if items[x]['zigbee_short'] in zigbee_ids:
                raise Exception(f"Device ID {item['id']} is not unique!")
            zigbee_ids.append(items[x]['zigbee_short'])

    # Generate THINGS
    conf_str = [PREAMBULA]
    for item in items:
        # Zigbee2mqtt device?
        if 'zigbee' in item['type']['types']:
            conf_str.extend(device_comment(item))
            conf_str.append(
                f"Thing mqtt:topic:openhab:{item['mqtt_topic']} (mqtt:broker:openhab) {{")
            conf_str.append(
                f"\tChannels:")
            # Device has switch option
            if np.in1d(['lamp', 'plug'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : state ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.state\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-state.js\""
                    f"]"
                )
            # Device has remote option
            if np.in1d(['remote'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType string : action [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.action\", trigger=true]")
            # Device has dimmer
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : dim ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.brightness\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-brightness.js\", min=1, max=255"
                    f"]"
                )
            # Device has Color Temp control
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : ct ["
                    f"stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\""
                    f", transformationPattern=\"JSONPATH:$.color_temp\""
                    f", commandTopic=\"zigbee2mqtt/{item['zigbee_id']}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-color_temp.js\", min=150, max=500"
                    f"]"
                )
            # Device has Motion sensor
            if np.in1d(['motion'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : occupancy [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.occupancy\", on=\"true\", off=\"false\"]")
            # Device has Leak sensor
            if np.in1d(['leak'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : leak [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.water_leak\", on=\"true\", off=\"false\"]")
            # Device has Temp sensor
            if np.in1d(['temperature'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : temperature [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.temperature\"]")
            if np.in1d(['humidity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : humidity [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.humidity\"]")
            if np.in1d(['pressure'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : pressure [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.pressure\"]")
            # Some zigbee devices needs to be monitored
            if np.in1d(['activity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType datetime : activity [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JS:z2m-activity.js\"]")
            # Some zigbee devices report battery
            if np.in1d(['battery'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : battery [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.battery\"]")
            if np.in1d(['battery', 'battery_low'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : battery_low [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.battery_low\", on=\"true\", off=\"false\"]")
            # Some zigbee devices report battery voltage
            if np.in1d(['voltage'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : voltage [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.voltage\"]")
            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"\t\tType number : link [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.linkquality\"]")
            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"\t\tType switch : ota [stateTopic=\"zigbee2mqtt/{item['zigbee_id']}\", transformationPattern=\"JSONPATH:$.update_available\", on=\"true\", off=\"false\"]")
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
    conf_str = [PREAMBULA]
    all_items = []
    gen_rules = [PREAMBULA]  # Special rules for devices
    for item in items:
        conf_str.extend(device_comment(item))
        # Some devices have switch option
        if np.in1d(['lamp', 'plug'], item['type']['types']).any():
            device_icon = 'switch'
            if 'lamp' in item['type']['types']:
                device_icon = 'light'
            device_timout = ''
            if 'expire' in item:
                device_timout = f", expire=\"{item['expire']},command=OFF\""
            conf_str.append(
                f"Switch {item['id']}_sw \"{item['name']}\" <{device_icon}>"
                f"{device_groups(item,'sw')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:state\"{device_timout}}}"
            )
            all_items.append(f"Switch item={item['id']}_sw")
        # Some devices have motion option
        if np.in1d(['motion'], item['type']['types']).any():
            device_icon = 'motion'
            conf_str.append(
                f"Switch {item['id']}_occupancy \"{item['name']}\" <{device_icon}>"
                f"{device_groups(item,'occupancy')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:occupancy\"}}"
            )
        # Some devices have leak option
        if np.in1d(['leak'], item['type']['types']).any():
            device_icon = 'flow'
            conf_str.append(
                f"Switch {item['id']}_leak \"{item['name']}\" <{device_icon}>"
                f"{device_groups(item,'leak')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:leak\"}}"
            )
        # Some devices have Temperature option
        if np.in1d(['temperature'], item['type']['types']).any():
            device_icon = 'temperature'
            conf_str.append(
                f"Number {item['id']}_temperature \"{item['name']} [%d °C]\" <{device_icon}>"
                f"{device_groups(item,'temperature')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:temperature\"}}"
            )
        # Some devices have Humidity option
        if np.in1d(['humidity'], item['type']['types']).any():
            device_icon = 'humidity'
            conf_str.append(
                f"Number {item['id']}_humidity \"{item['name']} [%d %%]\" <{device_icon}>"
                f"{device_groups(item,'humidity')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:humidity\"}}"
            )
        # Some devices have Pressure option
        if np.in1d(['pressure'], item['type']['types']).any():
            device_icon = 'pressure'
            conf_str.append(
                f"Number {item['id']}_pressure \"{item['name']} [%d hPa]\" <{device_icon}>"
                f"{device_groups(item,'pressure')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:pressure\"}}"
            )
        # Special Zigbee things
        if np.in1d(['zigbee'], item['type']['types']).any():
            # All Zigbee lamps have dimmer built-in
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_dim \"{item['name']} DIM [%d %%]\" <{device_icon}>"
                    f"{device_groups(item,'dim')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:dim\"}}"
                )
                all_items.append(f"Slider item={item['id']}_dim")

            # Zigbee color temperature
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_ct \"{item['name']} CT [JS(display-mired.js):%s]\" <colorwheel>"
                    f"{device_groups(item,'ct')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ct\"}}"
                )
                all_items.append(f"Slider item={item['id']}_ct")
                gen_rules.append(
                    f"""
// Device should apply saved color temp when ON
rule "{item['name']} apply color on ON"
when
    Item {item['id']}_sw changed to ON
then
	{item['id']}_ct.sendCommand({item['id']}_ct.state as Number)
end
"""
                )

            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"Number {item['id']}_link \"{item['name']} [%d]\""
                f" <network> (g_zigbee_link) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:link\"}}"
            )

            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"Switch {item['id']}_ota \"{item['name']} [%s]\""
                f" <flowpipe> (g_zigbee_ota) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ota\"}}"
            )

            # Some zigbee devices report battery
            if 'battery' in item['type']['types']:
                conf_str.append(
                    f"Number {item['id']}_battery \"{item['name']} [%d %%]\""
                    f" <battery> (g_battery_level) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery\"}}"
                )
            if np.in1d(['battery', 'battery_low'], item['type']['types']).any():
                conf_str.append(
                    f"Switch {item['id']}_battery_low \"{item['name']} [MAP(lowbat.map):%s]\""
                    f" <lowbattery> (g_battery_low) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery_low\"}}"
                )

            # ... and it's voltage
            if 'voltage' in item['type']['types']:
                conf_str.append(
                    f"Number {item['id']}_voltage \"{item['name']} [%d mV]\""
                    f" <energy> {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:voltage\"}}"
                )

            # Some zigbee devices report activity
            if 'activity' in item['type']['types']:
                conf_str.append(
                    f"DateTime {item['id']}_activity \"{item['name']} [JS(display-activity.js):%s]\""
                    f" <time> (g_zigbee_activity) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:activity\"}}"
                )

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'items', 'gen.items'), 'w')
        f.write(conf_str)
        f.close()

    # Write test sitemap
    test_sitemap = PREAMBULA + """
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
