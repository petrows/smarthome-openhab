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
import yaml
from pprint import pp

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

# Reserve:
# 0xec1bbdfffe9abfde - Ikea WW 860 (offline shop)
# 0x14b457fffe6383e5 - TRADFRI LED bulb E14/E26/E27 600 lumen, dimmable, color, opal white (ebay)
# 0x000d6ffffe12e11b - Ikea CT 1000 (ebay)
# 0x14b457fffe399241 - Ikea CT 1000 (ebay)
# 0xec1bbdfffe4695b5 - Ikea WW 806 (ebay)
# 0x60a423fffe4b9138 - Aldi LIGHTWAY smart home LED-lamp - filament (F122SB62H22A4.5W) (Aldi 2020-02-27)
# 0x60a423fffe4b91cf - Aldi LIGHTWAY smart home LED-lamp - filament (F122SB62H22A4.5W) (Aldi 2020-03-02)
# 0x847127fffe0c873b - TuYa Wall switch module (WHD02) (aliexpress 2020-04-09)
# 0x00158d0006b7aa81 - Xiaomi Aqara water leak sensor (SJCGQ11LM) (aliexpress 2020-06-18)
# 0x5c0272fffedc2f41 - TuYa Radiator valve with thermostat (TS0601_thermostat) (aliexpress 2020-06-18)
# 0x0c4314fffe73bf1f - Silvercerst thermostat (ebay 2021-12-30)
# 0x0c4314fffe62f090 - Silvercerst thermostat (ebay 2021-12-30)
# 0x0c4314fffe73c43f - Silvercerst thermostat (ebay 2022-01-07)
# 0x04cd15fffe6bf002 - Ikea 1055 lm (IKEA 2022-03-18)
# 0x04cd15fffe35e43a - Ikea 1055 lm (IKEA 2022-03-18) - defekt (noise) - return to Ikea 2022-03-19
# 0x04cd15fffe6d57dc - Ikea styrbar (IKEA 2022-03-18)
# 0x04cd15fffe73ecb6 - Ikea 1055 lm (IKEA 2022-03-19)
# 0x04cd15fffe35f24e - Ikea 1055 lm (IKEA 2022-03-19)
# 0x04cd15fffe75c518 - Ikea styrbar (IKEA 2022-03-19)
# 0x04cd15fffe789098 - Ikea styrbar (IKEA 2022-03-19)
# 0x0c4314fffe5c6913 - Silvercerst thermostat (ebay 2022-03-22)
# 0xa4c138f5460e22dd - Tuya temperature sensor TS0201 (aliexpress 2022-03-31)
# 0xa4c1383cc92cbbd2 - Tuya temperature sensor TS0201 (aliexpress 2022-03-31)
# 0xa4c1386df39045f6 - Tuya temperature sensor TS0201 (aliexpress 2022-03-31)
# 0x9035eafffe20e847 - TRADFRI LED bulb E27 WW clear 250 lumen, dimmable (Ikea 2022-08-10)
# 0x9035eafffe1b9fcc - TRADFRI LED bulb E27 WW clear 250 lumen, dimmable (Ikea 2022-08-10)
# 0x04cd15fffe7a35b5 - TRADFRI LED bulb E27 WW clear 250 lumen, dimmable (Ikea 2022-08-10)
# 0x04cd15fffe873cb7 - Ikea move sensor
# 0x8cf681fffe36d14e - TRADFRI E1766 Open/Close Remote (from Marina E.)
# 0xcc86ecfffea0c7cb - Livarno Home LED ceiling light (Lidl 2023-01-31)

# Items defentition
items = [
    # Test
    {
        'name': "Sturbar test",
        'id': "sturbar_test",
        'zigbee_id': '0x04cd15fffe6d57dc',
        'type': DEVICES.IKEA_TRADFRI_STYRBAR,
    },
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
        'zigbee_id': '0x14b457fffe399241',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'groups': {
            'sw': ['g_light_all', 'balkon_light'],
            'dim': ['balkon_light_dim'],
            'ct': ['balkon_light_ct'],
        }
    },
    {
        'name': "Garten wasser remote",
        'id': "garten_wasser_remote",
        'zigbee_id': '0xccccccfffe58f1c3',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    # EG (Corridor)
    # {
    #     'name': "Corridor main light",
    #     'id': "flur_light",
    #     'type': DEVICES.TASMOTA_SONOFF_MINI,
    # },
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
    {
        'name': "EG Decor light",
        'id': "eg_decoration_light",
        'zigbee_id': '0x9035eafffe20e847',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_auto'],
            'dim': ['g_dim_eg_auto'],
        }
    },
    {
        'name': "Entrance Door sensor",
        'id': "eg_main_door",
        'zigbee_id': '0xa4c138182f60d651',
        'type': DEVICES.TUYA_WINDOW_SENSOR_TS0203,
    },
    # EG (Closet)
    {
        'name': "BZ Light (toilet)",
        'id': "bz_light_1",
        'zigbee_id': '0xcc86ecfffea0c7cb',
        'type': DEVICES.LIVARNO_CELLING,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_bz', 'bz_main_light'],
            'dim': ['g_light_bz_dim'],
            'ct': ['g_light_astro_color', 'g_light_bz_ct'],
            'color': ['g_light_bz_color'],
        }
    },
    {
        'name': "BZ Light (shower)",
        'id': "bz_light_2",
        'zigbee_id': '0x04cd15fffedb319f',
        'type': DEVICES.LIVARNO_CELLING,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_bz', 'bz_main_light'],
            'dim': ['g_light_bz_dim'],
            'ct': ['g_light_astro_color', 'g_light_bz_ct'],
            'color': ['g_light_bz_color'],
        }
    },
    {
        'name': "BZ Mirror",
        'id': "bz_mirror",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'groups': {
            'POWER': ['g_light_all', 'g_light_eg', 'g_light_eg_bz'],
        },
        'channels': {
            'POWER': {
                'id': 'bz_mirror',
                'name': 'BZ Mirror',
            }
        }
    },
    {
        'name': "BZ Mirror switch",
        'id': "bz_mirror_switch",
        'zigbee_id': '0xccccccfffef0356e',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "BZ Light Control",
        'id': "bz_light_switch",
        'zigbee_id': '0x003c84fffe132b20',
        'type': DEVICES.IKEA_TRADFRI_STYRBAR,
    },
    # EG (Theater)
    {
        'name': "NS Climate",
        'id': "ns_climate",
        'zigbee_id': '0x00158d0001b95e08',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },

    {
        'name': "NS Boost power",
        'id': "ns_heating_boost_power",
        'zigbee_id': '0x7cb03eaa0a0a1103',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'expire': '1h'
    },
    {
        'name': "NS Night lamp",
        'id': "ns_night_lamp",
        'zigbee_id': '0xec1bbdfffe9abfde',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_ns'],
        }
    },
    {
        'name': "NS Projector",
        'id': "ns_projector_power",
        'zigbee_id': '0x7cb03eaa0a094d1d',
        'type': DEVICES.OSRAM_SMART_PLUG,
    },
    {
        'name': "NS Window 2",
        'id': "ns_window_2",
        'zigbee_id': '0xa4c138f1bf27592c',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['ns_windows'],
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
    # EG (Bedroom)
    {
        'name': "SZ Climate",
        'id': "sz_climate",
        'zigbee_id': '0x847127fffec6acc3',
        'type': DEVICES.TUYA_TEMPERATURE_SENSOR_TS0201,
    },
    {
        'name': "Bedroom remote",
        'id': "sz_remote",
        'zigbee_id': '0x14b457fffe7e2305',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "Bedroom curtains remote",
        'id': "sz_curtain_remote",
        'zigbee_id': '0x8cf681fffe36d14e',
        'type': DEVICES.IKEA_TRADFRI_CURTAIN_REMOTE,
    },
    {
        'name': "Bedroom night mode",
        'id': "sz_night_mode_remote",
        'zigbee_id': '0x2c1165fffe30cf8f',
        'type': DEVICES.SILVERCREST_SMART_BUTTON,
    },
    {
        'name': "SZ Bed 1",
        'id': "sz_bed_light_1",
        'zigbee_id': '0x04cd15fffe7a35b5',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_sz', 'sz_bed_light'],
            'dim': ['sz_bed_light_dim'],
        }
    },
    {
        'name': "SZ Bed 2",
        'id': "sz_bed_light_2",
        'zigbee_id': '0x9035eafffe1b9fcc',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_250,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_sz', 'sz_bed_light'],
            'dim': ['sz_bed_light_dim'],
        }
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
    {
        'name': "SZ Window 1",
        'id': "sz_window_1",
        'zigbee_id': '0xa4c13804963f4ccf',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['sz_windows'],
        }
    },
    {
        'name': "SZ Window Door",
        'id': "sz_window_door",
        'zigbee_id': '0xa4c138fbdde6b200',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['sz_windows'],
        }
    },
    {
        'name': "SZ CO2",
        'id': "sz_co2",
        'type': DEVICES.PETROWS_CO2_SENSOR,
        'device_id': '5C:CF:7F:68:19:46',
    },
    # EG (Kitchen)
    {
        'name': "KU Climate",
        'id': "ku_climate",
        'zigbee_id': '0x00158d0001b95fc4',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
    {
        'name': "KU Light Button (Spüle)",
        'id': "ku_light_switch_spule",
        'zigbee_id': '0x00158d0001be5b2d',
        'type': DEVICES.XIAOMI_BUTTON,
    },
    {
        'name': "KU Light Button (Kochfield)",
        'id': "ku_light_switch_kochfeld",
        'zigbee_id': '0x680ae2fffeaf18d4',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    {
        'name': "KU Light Arbeit",
        'id': "ku_light_arbeitplatte",
        'zigbee_id': '0xec1bbdfffea37757',
        'type': DEVICES.SILVERCREST_SMART_PLUG,
        'expire': '3h',
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_ku', 'g_light_eg_ku_main'],
        }
    },
    {
        'name': "KU Light Table SW",
        'id': "ku_light_table_switch",
        'zigbee_id': '0x04cd15fffe789098',
        'type': DEVICES.IKEA_TRADFRI_STYRBAR,
    },
    {
        'name': "KU Light Table",
        'id': "ku_light_table",
        'zigbee_id': '0xec1bbdfffe4695b5',
        'type': DEVICES.IKEA_TRADFRI_LAMP_W_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_ku'],
        }
    },
    {
        'name': "KU Light SW",
        'id': "ku_light_switch",
        'zigbee_id': '0x842e14fffe1267fb',
        'type': DEVICES.TUYA_WALL_SWITCH_TS0601,
        'channels': {
            'l1': {
                'id': 'ku_light_switch_haupt',
                'name': 'KU Light Haupt (Wall SW)',
                'groups': {
                    'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_ku', 'g_light_eg_ku_main'],
                }
            },
            'l2': {
                'id': 'ku_light_switch_arbeit',
                'name': 'KU Light Arbeit (Wall SW)',
                'expire': '3h',
                'groups': {
                    'sw': ['g_light_all', 'g_light_eg', 'g_light_eg_ku', 'g_light_eg_ku_main'],
                }
            },
        }
    },
    {
        'name': "KU Window Door",
        'id': "ku_window_door",
        'zigbee_id': '0xa4c1389dec8b9204',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['ku_windows'],
        }
    },
    # Ladder (Treppe)
    {
        'name': "Treppe Door sensor",
        'id': "treppe_door_sensor",
        'zigbee_id': '0xccccccfffed82b91',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
    },
    {
        'name': "Treppe Up switch",
        'id': "treppe_up_switch",
        'zigbee_id': '0x680ae2fffe1a92f3',
        'type': DEVICES.IKEA_TRADFRI_ON_OFF,
    },
    {
        'name': "Treppe Down switch",
        'id': "treppe_down_switch",
        'zigbee_id': '0x04cd15fffe75c518',
        'type': DEVICES.IKEA_TRADFRI_STYRBAR,
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
    {
        'name': "Treppe climate",
        'id': "treppe_climate",
        'zigbee_id': '0xa4c1383cc92cbbd2',
        'type': DEVICES.TUYA_TEMPERATURE_SENSOR_TS0201,
    },
    # KG
    {
        'name': "KG Window 1",
        'id': "kg_window_1",
        'zigbee_id': '0xccccccfffed82ba3',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['kg_windows'],
        }
    },
    {
        'name': "KG Window 2",
        'id': "kg_window_2",
        'zigbee_id': '0xa4c1381a072fcf8b',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['kg_windows', 'g_windows_skip_off'],
        }
    },
    {
        'name': "KG Cabinet door",
        'id': "kg_cabinet_door",
        'zigbee_id': '0xa4c138312d2c455f',
        'type': DEVICES.TUYA_WINDOW_SENSOR,
        'groups': {
            'contact': ['kg_windows', 'g_windows_skip_off'],
        }
    },
    {
        'name': "KG Climate",
        'id': "kg_climate",
        'zigbee_id': '0x00158d0001b95e02',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
    {
        'name': "Petro Desktop up light 1",
        'id': "desktop_petro_up_light_1",
        'zigbee_id': '0x04cd15fffe35f24e',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum', 'g_light_kg_desktop'],
            'ct': ['g_light_astro_color', 'g_light_kg_desktop_color'],
            'dim': ['g_light_kg_desktop_dim'],
        }
    },
    {
        'name': "Petro Desktop up light 2",
        'id': "desktop_petro_up_light_2",
        'zigbee_id': '0x04cd15fffe6bf002',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum', 'g_light_kg_desktop'],
            'ct': ['g_light_astro_color', 'g_light_kg_desktop_color'],
            'dim': ['g_light_kg_desktop_dim'],
        }
    },
    {
        'name': "Petro Desktop up light 3",
        'id': "desktop_petro_up_light_3",
        'zigbee_id': '0x04cd15fffe73ecb6',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CT_1000,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum', 'g_light_kg_desktop'],
            'ct': ['g_light_astro_color', 'g_light_kg_desktop_color'],
            'dim': ['g_light_kg_desktop_dim'],
        }
    },
    {
        'name': "Petro Desktop light",
        'id': "desktop_petro_light",
        'zigbee_id': '0xccccccfffed8ef9d',
        'type': DEVICES.IKEA_TRADFRI_LAMP_CLEAR_806,
        'groups': {
            'sw': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum'],
            'ct': ['g_light_astro_color'],
        }
    },
    {
        'name': "Petro Desktop PC",
        'id': "desktop_petro_pc_power",
        'zigbee_id': '0x847127fffe0c873b',
        'type': DEVICES.TUYA_SWITCH_TS0001,
    },
    {
        'name': "Petro Desktop remote",
        'id': "desktop_petro_remote",
        'zigbee_id': '0x000d6ffffee8357d',
        'type': DEVICES.IKEA_TRADFRI_REMOTE,
    },
    # Hobby Raum (Flür)
    {
        'name': "KG Hobbyraum (Flür)",
        'id': "kg_main1_light",
        'type': DEVICES.TASMOTA_SONOFF_TOUCH_EU1,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum', 'g_light_kg_auto'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_main1_light',
                'name': 'KG Hobbyraum (Flür)',
            }
        }
    },
    # Hobby Raum (Haupt)
    {
        'name': "KG Hobbyraum (Haupt)",
        'id': "kg_main2_light",
        'type': DEVICES.TASMOTA_SONOFF_TOUCH_EU1,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg', 'g_light_kg_hobbyraum'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_main2_light',
                'name': 'KG Hobbyraum (Haupt)',
            }
        }
    },
    {
        'name': "KG Heuzung (Haupt)",
        'id': "kg_hz_main_light",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_hz_main_light',
                'name': 'KG Heuzung (Haupt)',
                'expire': '1h',
            }
        }
    },
    # Garten wassering
    {
        'name': "Garden water",
        'id': "garten_wasser_sw",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'channels': {
            'POWER': {
                'id': 'garten_wasser_sw',
                'name': 'Garden water',
                'expire': '1h',
            }
        }
    },
    {
        'name': "Warehouse 3 leak",
        'id': "garten_wasser_leak",
        'zigbee_id': '0x00158d0006b7aa81',
        'type': DEVICES.XIAOMI_AQARA_LEAK_V1,
    },
    # Lagere
    {
        'name': "KG Lager 1 (Haupt)",
        'id': "kg_lager1_main_light",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_lager1_main_light',
                'name': 'KG Lager 1 (Haupt)',
                'expire': '1h',
            }
        }
    },
    {
        'name': "KG Lager 3 Climate",
        'id': "kg_lager3_climate",
        'zigbee_id': '0x00158d0001c19a6b',
        'type': DEVICES.XIAOMI_AQARA_V2,
    },
    {
        'name': "KG Lager 3 motion",
        'id': "kg_lager3_motion",
        'zigbee_id': '0x04cd15fffe873cb7',
        'type': DEVICES.IKEA_TRADFRI_MOTION_SENSOR,
    },
    {
        'name': "KG Lager 3 (Haupt)",
        'id': "kg_lager3_main_light",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_lager3_main_light',
                'name': 'KG Lager 3 (Haupt)',
                'expire': '1h',
            }
        }
    },
    {
        'name': "KG Lager 4 (Haupt)",
        'id': "kg_lager4_main_light",
        'type': DEVICES.TASMOTA_SONOFF_MINI,
        'groups': {
            'POWER': ['g_light_all', 'g_light_kg'],
        },
        'channels': {
            'POWER': {
                'id': 'kg_lager4_main_light',
                'name': 'KG Lager 4 (Haupt)',
                'expire': '1h',
            }
        }
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
        'name': "Warehouse 4 leak",
        'id': "kg_lager4_leak",
        'zigbee_id': '0x00158d000488052c',
        'type': DEVICES.XIAOMI_AQARA_LEAK_V1,
    },
    # Heating
    {
        'name': "FS heating",
        'id': "fs_heating",
        'zigbee_id': '0x0c4314fffe73c43f',
        'type': DEVICES.SILVERCREST_THERMOSTAT_368308_2010,
        'groups': {
            'thermostat': ['g_hz_all', 'g_hz_auto', 'g_hz_fs'],
            'position': ['g_hz_valve'],
        }
    },
    {
        'name': "NS heating",
        'id': "ns_heating",
        'zigbee_id': '0x0c4314fffe62f090',
        'type': DEVICES.SILVERCREST_THERMOSTAT_368308_2010,
        'groups': {
            'thermostat': ['g_hz_all', 'g_hz_auto', 'g_hz_ns'],
            'position': ['g_hz_valve'],
        }
    },
    {
        'name': "KU heating",
        'id': "ku_heating",
        'zigbee_id': '0x0c4314fffe73bf1f',
        'type': DEVICES.SILVERCREST_THERMOSTAT_368308_2010,
        'groups': {
            'thermostat': ['g_hz_all', 'g_hz_auto', 'g_hz_ku'],
            'position': ['g_hz_valve'],
        }
    },
    {
        'name': "SZ heating",
        'id': "sz_heating",
        'zigbee_id': '0x5c0272fffedc2f41',
        'type': DEVICES.TUYA_THERMOSTAT_VALVE,
        'groups': {
            'thermostat': ['g_hz_all', 'g_hz_auto', 'g_hz_sz'],
            'position': ['g_hz_valve'],
        }
    },
    {
        'name': "KG heating",
        'id': "kg_heating",
        'zigbee_id': '0x0c4314fffe5c6913',
        'type': DEVICES.SILVERCREST_THERMOSTAT_368308_2010,
        'groups': {
            'thermostat': ['g_hz_all', 'g_hz_auto', 'g_hz_kg'],
            'position': ['g_hz_valve'],
        }
    },

    # Christmas lights
    # Set group g_light_christmas - only for holidays!!!
    {
        'name': "FS Christmas light",
        'id': "fs_christmas_light",
        'zigbee_id': '0x7cb03eaa0a093a8b',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'],
        }
    },
    {
        'name': "NS Christmas light",
        'id': "ns_christmas_light",
        'zigbee_id': '0x7cb03eaa0a094303',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'],
        }
    },
    {
        'name': "Balkon Christmas light",
        'id': "balkon_christmas_light",
        'zigbee_id': '0x7cb03eaa0a094bf2',
        'type': DEVICES.OSRAM_SMART_PLUG,
        'groups': {
            'sw': ['g_light_christmas'],
        }
    },
    # =====================
    {
        'name': "Test remote",
        'id': "test_ikea_remote",
        'zigbee_id': '0x003c84fffe16f988',
        'type': DEVICES.IKEA_TRADFRI_STYRBAR,
    },
]


def device_label(item):
    device_id = ''
    if np.in1d(['zigbee'], item['type']['types']).any():
        device_id = item['zigbee_id']
    else:
        device_id = item['id']
    return f"{item['name']} ({device_id})"


def device_comment(item):
    conf_str = []
    conf_str.append(f"// {device_label(item)}")
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
    zigbee_devices_list = {}
    for x, item in enumerate(items):
        if item['id'] in item_ids:
            raise Exception(f"Device ID {item['id']} is not unique!")
        item_ids.append(item['id'])
        items[x]['mqtt_topic'] = f"{items[x]['id']}"
        if np.in1d(['zigbee'], item['type']['types']).any():
            # Add to all Zigbee items generated MQTT topic like "zigbee-XXXX"
            items[x]['zigbee_short'] = device_short_id(item['zigbee_id'])
            # Add ids to check conflicts
            if items[x]['zigbee_short'] in zigbee_ids:
                raise Exception(f"Device ID {item['id']} is not unique!")
            zigbee_ids.append(items[x]['zigbee_short'])
            zigbee_devices_yaml = {'friendly_name': item['id']}
            if 'simulated_brightness' in item['type']['types']:
                zigbee_devices_yaml['simulated_brightness'] = list()
            zigbee_devices_list[item['zigbee_id']] = zigbee_devices_yaml

    # Generate THINGS
    conf_str = [PREAMBULA]
    for item in items:
        # petro.ws device?
        if 'petrows' in item['type']['types']:
            device_topic_prefix = "petrows/" + item['device_id']
            conf_str.extend(device_comment(item))
            conf_str.append(
                f"Thing mqtt:topic:openhab:{item['mqtt_topic']} \"{item['name']}\" (mqtt:broker:openhab) {{")
            conf_str.append(
                f"\tChannels:")

            # CO₂ sensor
            if np.in1d(['co2'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : co2 ["
                    f"stateTopic=\"{device_topic_prefix}/STATE\""
                    f", transformationPattern=\"JSONPATH:$.S8.CO2\""
                    f"]"
                )
                conf_str.append(
                    f"\t\tType switch : co2_led ["
                    f"stateTopic=\"{device_topic_prefix}/STATE\""
                    f", transformationPattern=\"JSONPATH:$.S8.led\", on=\"1\", off=\"0\""
                    f"]"
                )

            # Standard signal values
            conf_str.append(
                f"\t\tType number : rssi ["
                f"stateTopic=\"{device_topic_prefix}/STATE\""
                f", transformationPattern=\"JSONPATH:$.Wifi.RSSI\""
                f"]"
            )
            conf_str.append(
                f"\t\tType string : bssid ["
                f"stateTopic=\"{device_topic_prefix}/STATE\""
                f", transformationPattern=\"JSONPATH:$.Wifi.BSSId\""
                f"]"
            )
            # Common monitoring
            if np.in1d(['activity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType datetime : activity [stateTopic=\"{device_topic_prefix}/STATE\", transformationPattern=\"JS:z2m-activity.js\"]")

            conf_str.append(f"}}")

        # tasmota-wifi device?
        if 'tasmota' in item['type']['types']:
            conf_str.extend(device_comment(item))
            conf_str.append(
                f"Thing mqtt:topic:openhab:{item['mqtt_topic']} \"{item['name']}\" (mqtt:broker:openhab) {{")
            conf_str.append(
                f"\tChannels:")

            # Iterate through avaliable channels
            for channel in item['type']['tasmota_channels']:
                channel_type = channel['type']
                if channel_type == 'co2':
                    conf_str.append(
                        f"\t\tType number : {channel['id']} ["
                        f"stateTopic=\"tele/{item['id']}/SENSOR\""
                        f", transformationPattern=\"JSONPATH:$.{channel['id']}.CarbonDioxide\""
                        f"]"
                    )
                else:
                    command_opts = ''
                    if 'switch' == channel['type']:
                        command_opts = ", on=\"ON\", off=\"OFF\""
                    if 'dimmer' == channel['type']:
                        command_opts = ", min=1, max=100"
                    conf_str.append(
                        f"\t\tType {channel['type']} : {channel['id']} ["
                        f"stateTopic=\"stat/{item['id']}/RESULT\""
                        f", transformationPattern=\"JSONPATH:$.{channel['id']}\""
                        f", commandTopic=\"cmnd/{item['id']}/{channel['id']}\""
                        f"{command_opts}"
                        f"]"
                    )

            # Standard signal values
            conf_str.append(
                f"\t\tType number : rssi ["
                f"stateTopic=\"tele/{item['id']}/STATE\""
                f", transformationPattern=\"JSONPATH:$.Wifi.RSSI\""
                f"]"
            )
            conf_str.append(
                f"\t\tType string : bssid ["
                f"stateTopic=\"tele/{item['id']}/STATE\""
                f", transformationPattern=\"JSONPATH:$.Wifi.BSSId\""
                f"]"
            )
            conf_str.append(
                f"\t\tType number : la ["
                f"stateTopic=\"tele/{item['id']}/STATE\""
                f", transformationPattern=\"JSONPATH:$.LoadAvg\""
                f"]"
            )

            # Some wifi devices needs to be monitored
            if np.in1d(['activity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType datetime : activity [stateTopic=\"tele/{item['id']}/STATE\", transformationPattern=\"JS:z2m-activity.js\"]")

            conf_str.append(f"}}")

        # Zigbee2mqtt device?
        if 'zigbee' in item['type']['types']:
            conf_str.extend(device_comment(item))
            conf_str.append(
                f"Thing mqtt:topic:openhab:{item['mqtt_topic']} \"{item['name']}\" (mqtt:broker:openhab) {{")
            conf_str.append(
                f"\tChannels:")
            zigbe_mqtt_topic = f"zigbee2mqtt/{item['id']}"
            # Device has switch option
            if np.in1d(['lamp', 'plug'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : state ["
                    f"stateTopic=\"{zigbe_mqtt_topic}\""
                    f", transformationPattern=\"JSONPATH:$.state\""
                    f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-state.js\""
                    f"]"
                )
            # Device has switch (multi-gang) option
            if np.in1d(['plug_mt'], item['type']['types']).any():
                # Iterate through avaliable channels
                for channel_id, channel in item['channels'].items():
                    conf_str.append(
                        f"\t\tType switch : state_{channel_id} ["
                        f"stateTopic=\"{zigbe_mqtt_topic}\""
                        f", transformationPattern=\"JSONPATH:$.state_{channel_id}\""
                        f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                        f", formatBeforePublish=\"{{\\\"state_{channel_id}\\\":\\\"%s\\\"}}\""
                        f"]"
                    )
            # Device has remote option
            if np.in1d(['remote'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType string : action [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*\\\"action\\\".*)∩JSONPATH:$.action\", trigger=true]")
            if np.in1d(['simulated_brightness'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : dim [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*\\\"action_brightness_delta\\\".*)∩JSONPATH:$.brightness\", min=0, max=255]")

            # Device has dimmer
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : dim ["
                    f"stateTopic=\"{zigbe_mqtt_topic}\""
                    f", transformationPattern=\"JSONPATH:$.brightness\""
                    f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-brightness.js\", min=1, max=255"
                    f"]"
                )
            # Device has Color Temp control
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType dimmer : ct ["
                    f"stateTopic=\"{zigbe_mqtt_topic}\""
                    f", transformationPattern=\"JSONPATH:$.color_temp\""
                    f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-color_temp.js\", min=150, max=500"
                    f"]"
                )
            # Device has Color control
            if np.in1d(['color'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType color : color ["
                    # f"stateTopic=\"{zigbe_mqtt_topic}\""
                    # f", transformationPattern=\"JSONPATH:$.color_xy\""
                    f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-color_xy.js\""
                    f"]"
                )
                conf_str.append(
                    f"\t\tType string : color_mode ["
                    f", stateTopic=\"{zigbe_mqtt_topic}\""
                    f", transformationPattern=\"JSONPATH:$.color_mode\""
                    f"]"
                )
            # Device has Thermostat control
            if np.in1d(['thermostat'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : thermostat ["
                    f"stateTopic=\"{zigbe_mqtt_topic}\""
                    f", transformationPattern=\"JSONPATH:$.current_heating_setpoint\""
                    f", commandTopic=\"{zigbe_mqtt_topic}/set\""
                    f", transformationPatternOut=\"JS:z2m-command-thermostat-setpoint.js\""
                    f", unit=\"°C\""
                    f"]"
                )

            # Device has Position sensor
            if np.in1d(['position'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : position [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.position\"]")

            # Device has Contact sensor (inverse OPEN/CLOSE logic)
            if np.in1d(['contact'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType contact : contact [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.contact\", on=\"false\", off=\"true\"]")

            # Device has Motion sensor
            if np.in1d(['motion'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : occupancy [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.occupancy\", on=\"true\", off=\"false\"]")
            # Device has Leak sensor
            if np.in1d(['leak'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType switch : leak [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.water_leak\", on=\"true\", off=\"false\"]")
            # Device has Temp sensor
            if np.in1d(['temperature'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : temperature [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JS:z2m-temperature.js\",unit=\"°C\"]")  # Could be different fields,sudo detect here

            if np.in1d(['humidity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : humidity [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.humidity\"]")
            if np.in1d(['pressure'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : pressure [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*pressure.*)∩JSONPATH:$.pressure\",unit=\"hPa\"]")
            # Some zigbee devices needs to be monitored
            if np.in1d(['activity'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType datetime : activity [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JS:z2m-activity.js\"]")
            # Some zigbee devices report battery OR battery_low signal
            if np.in1d(['battery'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : battery [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*battery.*)∩JSONPATH:$.battery\"]")
                conf_str.append(
                    f"\t\tType switch : battery_low [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*battery.*)∩JS:z2m-lowbatt.js\"]")
            else:
                if np.in1d(['battery_low'], item['type']['types']).any():
                    conf_str.append(
                        f"\t\tType switch : battery_low [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JSONPATH:$.battery_low\", on=\"true\", off=\"false\"]")
            # Some zigbee devices want custom battery signal
            if np.in1d(['battery_voltage'], item['type']['types']).any():
                batt_type = item['type']['batt_type']
                conf_str.append(
                    f"\t\tType switch : battery_low [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*battery.*)∩JS:z2m-batt-low-{batt_type}.js\"]")
            # Some zigbee devices report battery voltage
            if np.in1d(['voltage'], item['type']['types']).any():
                conf_str.append(
                    f"\t\tType number : voltage [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"JS:z2m-batt-mv.js\",unit=\"V\"]")
            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"\t\tType number : link [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*linkquality.*)∩JSONPATH:$.linkquality\"]")
            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"\t\tType switch : ota [stateTopic=\"{zigbe_mqtt_topic}\", transformationPattern=\"REGEX:(.*update_available.*)∩JSONPATH:$.update_available\", on=\"true\", off=\"false\"]")
            conf_str.append(
                f"}}")

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'things', 'gen_things.things'), 'w')
        f.write(conf_str)
        f.close()

    # Generate ITEMS
    conf_str = [PREAMBULA]
    all_items = []
    gen_rules = [PREAMBULA]  # Special rules for devices
    for item in items:
        conf_str.extend(device_comment(item))
        device_items = {
            'item': item,
            'items': []
        }
        all_items.append(device_items)

        # Petrows devices
        if np.in1d(['petrows'], item['type']['types']).any():
            if np.in1d(['co2'], item['type']['types']).any():
                device_icon = channel_cfg.get('icon', 'co2')
                conf_str.append(
                    f"Number:Dimensionless {item['id']} \"{item['name']} [%d ppm]\" <{device_icon}>"
                    f"{device_groups(item, 'co2')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:co2\"}}"
                )
                device_items['items'].append(f"Text item={item['id']}")
                conf_str.append(
                    f"Switch {item['id']}_led \"{item['name']} LED\" <alarm>"
                    f"{device_groups(item, 'co2_led')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:co2_led\"}}"
                )
                device_items['items'].append(f"Text item={item['id']}_led")

        # Tasmota devices
        if np.in1d(['tasmota'], item['type']['types']).any():
            # Iterate through avaliable channels
            for channel in item['type']['tasmota_channels']:
                channel_cfg = item['channels'][channel['id']]
                device_icon = channel_cfg.get('icon', 'light')
                if 'expire' in channel_cfg:
                    device_timout = f", expire=\"{channel_cfg['expire']},command=OFF\""
                if channel['type'] == 'switch':
                    conf_str.append(
                        f"Switch {channel_cfg['id']} \"{channel_cfg['name']}\" <{device_icon}>"
                        f"{device_groups(item, channel['id'])}"
                        f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:{channel['id']}\"{device_timout}}}"
                    )
                    device_items['items'].append(f"Switch item={item['id']}")
                if channel['type'] == 'co2':
                    conf_str.append(
                        f"Number:Dimensionless {channel_cfg['id']} \"{channel_cfg['name']}\" <{device_icon}>"
                        f"{device_groups(item, channel['id'])}"
                        f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:{channel['id']}\"{device_timout}}}"
                    )
                    device_items['items'].append(f"Text item={item['id']}")

        # Generic devices

        # SOme device have switch (multi-gang) option
        if np.in1d(['plug_mt'], item['type']['types']).any():
            # Iterate through avaliable channels
            for channel_id, channel in item['channels'].items():
                device_icon = 'light'
                if 'icon' in channel:
                    device_icon = channel['icon']
                device_timout = ''
                if 'expire' in channel:
                    device_timout = f", expire=\"{channel['expire']},command=OFF\""
                conf_str.append(
                    f"Switch {channel['id']}_sw \"{channel['name']}\" <{device_icon}>"
                    f"{device_groups(channel,'sw')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:state_{channel_id}\"{device_timout}}}"
                )
                device_items['items'].append(f"Switch item={channel['id']}_sw")

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
            device_items['items'].append(f"Switch item={item['id']}_sw")

        # Somde devices simulate brightness
        if np.in1d(['simulated_brightness'], item['type']['types']).any():
            device_icon = 'light'
            conf_str.append(
                f"Dimmer {item['id']}_dim \"{item['name']} DIM [%.0f %%]\" <{device_icon}>"
                f"{device_groups(item,'dim')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:dim\"}}"
            )
            device_items['items'].append(
                f"Text item={item['id']}_dim")

        # Some devices have thermostat
        if np.in1d(['thermostat'], item['type']['types']).any():
            device_icon = 'heatingt'
            conf_str.append(
                f"Number:Temperature {item['id']}_thermostat \"{item['name']} SET [%.0f %unit%]\" <{device_icon}>"
                f"{device_groups(item,'thermostat')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:thermostat\"}}"
            )
            device_items['items'].append(
                f"Setpoint item={item['id']}_thermostat minValue=5 maxValue=30 step=1")

        # Some devices have position option
        if np.in1d(['position'], item['type']['types']).any():
            device_icon = 'heating'
            conf_str.append(
                f"Number:Dimensionless {item['id']}_position \"{item['name']} POS [%.0f %%]\" <{device_icon}>"
                f"{device_groups(item,'position')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:position\"}}"
            )
            device_items['items'].append(
                f"Text item={item['id']}_position")

        # Some devices have contact option
        if np.in1d(['contact'], item['type']['types']).any():
            device_icon = 'door'
            conf_str.append(
                f"Contact {item['id']}_contact \"{item['name']} contact [%s]\" <{device_icon}>"
                f"{device_groups(item,'contact')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:contact\"}}"
            )
            device_items['items'].append(
                f"Text item={item['id']}_contact")

        # Some devices have motion option
        if np.in1d(['motion'], item['type']['types']).any():
            device_icon = 'motion'
            conf_str.append(
                f"Switch {item['id']}_occupancy \"{item['name']}\" <{device_icon}>"
                f"{device_groups(item,'occupancy')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:occupancy\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_occupancy")

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
                f"Number:Temperature {item['id']}_temperature \"{item['name']} [%.0f %unit%]\" <{device_icon}>"
                f"{device_groups(item,'temperature')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:temperature\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_temperature")

        # Some devices have Humidity option
        if np.in1d(['humidity'], item['type']['types']).any():
            device_icon = 'humidity'
            conf_str.append(
                f"Number:Dimensionless {item['id']}_humidity \"{item['name']} [%.0f %%]\" <{device_icon}>"
                f"{device_groups(item,'humidity')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:humidity\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_humidity")
        # Some devices have Pressure option
        if np.in1d(['pressure'], item['type']['types']).any():
            device_icon = 'pressure'
            conf_str.append(
                f"Number:Pressure {item['id']}_pressure \"{item['name']} [%.0f %unit%]\" <{device_icon}>"
                f"{device_groups(item,'pressure')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:pressure\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_pressure")

        # Special WiFi things
        if np.in1d(['rssi'], item['type']['types']).any():
            device_icon = 'network'
            conf_str.append(
                f"Number:Dimensionless {item['id']}_rssi \"{item['name']} RSSI [%.0f]\" <{device_icon}>"
                f"{device_groups(item,'rssi')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:rssi\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_rssi")

        if np.in1d(['bssid'], item['type']['types']).any():
            device_icon = 'network'
            conf_str.append(
                f"String {item['id']}_bssid \"{item['name']} BSSID [%s]\" <{device_icon}>"
                f"{device_groups(item,'bssid')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:bssid\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_bssid")

        if np.in1d(['la'], item['type']['types']).any():
            device_icon = 'energy'
            conf_str.append(
                f"Number:Dimensionless {item['id']}_la \"{item['name']} LA [%d]\" <{device_icon}>"
                f"{device_groups(item,'la')}"
                f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:la\"}}"
            )
            device_items['items'].append(f"Text item={item['id']}_la")

        # Some devices report activity
        if 'activity' in item['type']['types']:
            conf_str.append(
                f"DateTime {item['id']}_activity \"{item['name']} [JS(display-activity.js):%s]\""
                f" <time> (g_device_activity) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:activity\"}}"
            )

        # Special Zigbee things
        if np.in1d(['zigbee'], item['type']['types']).any():
            zigbe_mqtt_topic = f"zigbee2mqtt/{item['id']}"
            # All Zigbee lamps have dimmer built-in
            if np.in1d(['lamp'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_dim \"{item['name']} DIM [%d %%]\" <{device_icon}>"
                    f"{device_groups(item,'dim')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:dim\"}}"
                )
                device_items['items'].append(f"Slider item={item['id']}_dim")

            # Zigbee color temperature
            if np.in1d(['ct'], item['type']['types']).any():
                conf_str.append(
                    f"Dimmer {item['id']}_ct \"{item['name']} CT [JS(display-mired.js):%s]\" <colorwheel>"
                    f"{device_groups(item,'ct')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ct\"}}"
                )
                device_items['items'].append(f"Slider item={item['id']}_ct")
                gen_rules.append(
                    f"""
// Device should apply saved color temp when ON
rule "{item['name']} apply color on ON"
when
    Item {item['id']}_sw received command ON
then
    val ct_set = ({item['id']}_ct.state as Number).intValue
    Thread::sleep(1000)
    // Send CT command directly via MQTT, as some devices reports "old" values
    val mqtt_actions = getActions("mqtt","mqtt:broker:openhab")
    mqtt_actions.publishMQTT("{zigbe_mqtt_topic}/set", "{{\\\"color_temp\\\":" + ct_set.toString() + "}}")
end
"""
                )
            # Zigbee color
            if np.in1d(['color'], item['type']['types']).any():
                conf_str.append(
                    f"Color {item['id']}_color \"{item['name']} Color\" <colorwheel>"
                    f"{device_groups(item,'color')}"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:color\"}}"
                )
                conf_str.append(
                    f"String {item['id']}_color_mode \"{item['name']} Color mode [%s]\" <light>"
                    f" {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:color_mode\"}}"
                )
                device_items['items'].append(f"Colorpicker item={item['id']}_color")
                # Set to ON, when color mode, OFF to normal mode (CT)
                # Set to ON, when color mode, OFF to normal mode (CT)
                device_items['items'].append(f"Text item={item['id']}_color_mode")

            # All zigbee devices have Link Quality reported
            conf_str.append(
                f"Number:Dimensionless {item['id']}_link \"{item['name']} LINK [%d]\""
                f" <linkz> (g_zigbee_link) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:link\"}}"
            )
            device_items['items'].append(
                f"Text item={item['id']}_link icon=\"linkz\"")

            # All zigbee devices probably have some OTA updates reported
            conf_str.append(
                f"Switch {item['id']}_ota \"{item['name']} OTA [%s]\""
                f" <fire> (g_zigbee_ota) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:ota\"}}"
            )
            device_items['items'].append(
                f"Text item={item['id']}_ota icon=\"fire\"")

            # Some zigbee devices report battery
            if 'battery' in item['type']['types']:
                conf_str.append(
                    f"Number:Dimensionless {item['id']}_battery \"{item['name']} [%.0f %%]\""
                    f" <battery> (g_battery_level) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery\"}}"
                )
            if np.in1d(['battery', 'battery_low', 'battery_voltage'], item['type']['types']).any():
                conf_str.append(
                    f"Switch {item['id']}_battery_low \"{item['name']} [MAP(lowbat.map):%s]\""
                    f" <lowbattery> (g_battery_low) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:battery_low\"}}"
                )

            # ... and it's voltage
            if 'voltage' in item['type']['types']:
                conf_str.append(
                    f"Number:ElectricPotential {item['id']}_voltage \"{item['name']} [%.0f mV]\""
                    f" <energy> (g_battery_voltage) {{channel=\"mqtt:topic:openhab:{item['mqtt_topic']}:voltage\"}}"
                )

        conf_str.append('')
    # Write config
    conf_str = '\n'.join(conf_str)
    print(conf_str)
    if args.write:
        f = open(os.path.join(ROOT_PATH, 'items', 'gen_items.items'), 'w')
        f.write(conf_str)
        f.close()

    print(all_items)

    # Write test sitemap
    test_sitemap = PREAMBULA + """
sitemap gen label="GEN ITEMS"
{
"""
    for gen_item in all_items:
        if not gen_item['items']:
            continue
        test_sitemap += f"Frame label=\"{device_label(gen_item['item'])}\" {{\n"
        test_sitemap += "\n".join(gen_item['items'])
        test_sitemap += "\n}\n"

    test_sitemap += """
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
        f = open(os.path.join(ROOT_PATH, 'rules', 'gen_auto.rules'), 'w')
        f.write(gen_rules)
        f.close()

    # (re)Generate Zigbee devices list
    if args.write:
        device_yaml = {}
        # Load old devices config
        # Don not load enymore. Build our own new from config
        # device_yaml = yaml.load(
        #     open(
        #         os.path.join(ROOT_PATH, 'devices.yaml'),
        #         'r'
        #     ),
        #     Loader=yaml.FullLoader
        # )

        yaml.dump(
            zigbee_devices_list,
            open(
                os.path.join(ROOT_PATH, 'devices.yaml'),
                'w'
            )
        )
