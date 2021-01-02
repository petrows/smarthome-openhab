#!/usr/bin/env python3

import paho.mqtt.publish as publish
import requests
import argparse
import logging
import json
import dateparser

parser = argparse.ArgumentParser(description='Parse KVV app for timetable')

parser.add_argument(
    '--log', help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL', default='INFO')
parser.add_argument('--mqtt-host', help='MQTT broker host',
                    default='localhost')
parser.add_argument('--mqtt-port', help='MQTT broker port', default='1883')
parser.add_argument('--mqtt-user', help='MQTT broker user', default='user')
parser.add_argument(
    '--mqtt-pass', help='MQTT broker password', default='password')
parser.add_argument('--mqtt-topic', help='MQTT broker topic',
                    default='kvv-timetable')
parser.add_argument('--stop-id',
                    help='Stop id (please find proper one in https://live.kvv.de/'
                    ' and copy it from URL), value like de:XXXX:YYYY, default is Marktplatz',
                    default='de:8212:1')

args = parser.parse_args()

numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % numeric_level)
logging.basicConfig(level=numeric_level)

logging.debug(args)

mqtt_auth = {'username': args.mqtt_user, 'password': args.mqtt_pass}

page = requests.get(
    'https://live.kvv.de/webapp/departures/bystop/'+args.stop_id+'?maxInfos=10&key=377d840e54b59adbe53608ba1aad70e8')

#print(page.content.decode('UTF-8'))

data = json.loads(page.content)
#f = open('test-kvv.json', 'r')
#data = json.loads(f.read())

# Publish 10 next trams
for idx, route in enumerate(data['departures']):
    if route['time'] == '0':
        route['time'] = 'now'
    route['tms'] = dateparser.parse('in ' + route['time']).isoformat()
    route['destination_city'] = \
        'KA → ' + route['destination'] if route['direction'] == '1' \
        else route['destination']
    route['direction_text'] = '→KA' if route['direction'] == '1' else '←KA'
    route['summary_text'] = f"{route['destination_city']} | {route['time']}"

    payload = json.dumps(route)

    # Publish route to MQTT
    publish.single(args.mqtt_topic+'/route-'+str(idx), payload=payload, qos=0, retain=True, hostname=args.mqtt_host,
                   port=int(args.mqtt_port), client_id="KVV-Routes", auth=mqtt_auth)

    #print(route)

#print(data)

#publish.single(args.mqtt_topic, payload=mes, qos=0, retain=True, hostname=args.mqtt_host,
#               port=int(args.mqtt_port), client_id="WeatherRadiationMeter", auth=mqtt_auth)
