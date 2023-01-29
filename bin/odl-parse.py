#!/usr/bin/env python3

from lxml import html
import paho.mqtt.publish as publish
import requests
import argparse
import logging
import sys

rad_level = 0.0001

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0',
}

parser = argparse.ArgumentParser(description='Parse radiation level')

parser.add_argument('plz', metavar='plz', type=int,
                    help='POstcode of measurment place, eg 76133')

parser.add_argument(
    '--log', help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL', default='INFO')
parser.add_argument('--mqtt-host', help='MQTT broker host', default='localhost')
parser.add_argument('--mqtt-port', help='MQTT broker port', default='1883')
parser.add_argument('--mqtt-user', help='MQTT broker user', default='user')
parser.add_argument('--mqtt-pass', help='MQTT broker password', default='password')
parser.add_argument('--mqtt-topic', help='MQTT broker topic', default='odl-radlevel')

args = parser.parse_args()

numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % numeric_level)
logging.basicConfig(level=numeric_level)

logging.debug(args)

mqtt_auth = {'username':args.mqtt_user, 'password':args.mqtt_pass}

api_url = 'https://www.imis.bfs.de/ogc/opendata/ows'
api_request = f'<GetFeature xmlns="http://www.opengis.net/wfs" service="WFS" version="1.1.0" outputFormat="application/json" viewParams="_dc:1674989865629;" xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengis.net/wfs/1.1.0/wfs.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><Query typeName="odlinfo_odl_1h_latest"><Filter xmlns="http://www.opengis.net/ogc"><PropertyIsEqualTo><PropertyName>plz</PropertyName><Literal>{args.plz}</Literal></PropertyIsEqualTo></Filter></Query></GetFeature>'

page = requests.post(api_url, data=api_request, headers=headers)

data = page.json()

number_found = data['numberMatched']

if not number_found:
    logging.error("0 results found for PLZ %d", args.plz)
    logging.error(
        "Select proper station here: https://odlinfo.bfs.de/ODL/DE/themen/wo-stehen-die-sonden/liste/liste_node.html")
    sys.exit(1)

station = data['features'][0]['properties']
value = station['value']

logging.debug("Using station: %s (%s)", station['name'], station['plz'])
logging.info("Value: %f", value)

publish.single(args.mqtt_topic, payload=value, qos=0, retain=True, hostname=args.mqtt_host,
               port=int(args.mqtt_port), client_id="WeatherRadiationMeter", auth=mqtt_auth)
