#!/usr/bin/env python3

import paho.mqtt.publish as publish
import requests
import argparse
import logging
import json
import time
import datetime
import dateparser
import xml.dom.minidom
from diskcache import Cache


def cache_get(station, date):
    filename = '/tmp/db-'+station+'-'+date.isoformat()+'.xml'


parser = argparse.ArgumentParser(description='Parse DB timetable')

parser.add_argument(
    '--log', help='Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL', default='INFO')
parser.add_argument('--mqtt-host', help='MQTT broker host',
                    default='localhost')
parser.add_argument('--mqtt-port', help='MQTT broker port', default='1883')
parser.add_argument('--mqtt-user', help='MQTT broker user', default='user')
parser.add_argument(
    '--mqtt-pass', help='MQTT broker password', default='password')
parser.add_argument('--mqtt-topic', help='MQTT broker topic',
                    default='db-timetable')
parser.add_argument('--stop-id',
                    help='Stop id (please find proper one in https://developer.deutschebahn.com/'
                    ' and copy it from URL), value "eva" numeric, default is Karlsruhe Hbf (8000191)',
                    default='8000191')
parser.add_argument('--api-key',
                    help='API key. Please find proper one in https://developer.deutschebahn.com/'
                    'it is free, just register there',
                    )
parser.add_argument('--size',
                    help='Try to find minimum trains amount (maximum 20 requests limit)',
                    default=4
                    )

args = parser.parse_args()

cache = Cache(directory='/tmp/db-timetable')

numeric_level = getattr(logging, args.log.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError('Invalid log level: %s' % numeric_level)
logging.basicConfig(level=numeric_level)

logging.debug(args)

mqtt_auth = {'username': args.mqtt_user, 'password': args.mqtt_pass}

# Find amount
trains = []
request_time = datetime.datetime.now()

for x in range(20):
    if len(trains) >= args.size:
        logging.debug(f"Reached max trains with {len(trains)} records")
        break

    cache_id = f"{args.stop_id}-{request_time.strftime('%Y-%m-%d-%H')}"

    logging.debug(f"Requesting table for {request_time.isoformat()}")

    data = cache.get(cache_id)

    if not data:
        logging.debug(f"Cache miss, reading from network")
        # f = open('test-db.xml', 'r')
        # data = f.read()

        headers = {"Authorization": f"Bearer {args.api_key}"}

        api_url = f"https://api.deutschebahn.com/timetables/v1/plan/{args.stop_id}/{request_time.strftime('%y%m%d')}/{request_time.strftime('%H')}"

        data = requests.get(api_url, headers=headers).content.decode('UTF-8')

        cache.set(cache_id, data, expire=86400)

        print(data)

    else:
        logging.debug(f"Cache used")

    doc = xml.dom.minidom.parseString(data)
    doc_trains = doc.getElementsByTagName("s")
    station = doc.getElementsByTagName("timetable")[0].getAttribute("station")
    for el in doc_trains:
        train_id = el.getAttribute("id")
        el_train = el.getElementsByTagName("tl")[0]

        train_number = '?'
        train_path = []
        train_dst = ''

        # Only arrives? (no DST)
        if not el.getElementsByTagName("dp"):
            # DST is current station
            el_depart = el.getElementsByTagName("ar")[0]
            train_path = []
            train_dst = station
        else:
            el_depart = el.getElementsByTagName("dp")[0]
            train_path = el_depart.getAttribute("ppth").split('|')
            train_dst = train_path[-1]

        # Avoid duplicates
        train_exists = False
        try:
            train_exists = next(x for x in trains if x["id"] == train_id)
        except:
            pass

        if train_exists:
            continue

        train = {}
        train['id'] = train_id
        train['type'] = el_train.getAttribute('c')
        train['number'] = el_depart.getAttribute("l")
        train['route'] = f"{train['type']}{train['number']}"
        train['path'] = train_path
        train['destination_city'] = train_dst
        train['tms'] = datetime.datetime.fromtimestamp(time.mktime(time.strptime(
            el_depart.getAttribute("pt"), '%y%m%d%H%M')))

        trains.append(train)

        logging.debug(train)

        # Next hour
        request_time += datetime.timedelta(hours=1)

# Sort data
trains.sort(key=lambda x: x.get('tms'), reverse=False)

# Publish trains
for idx, train in enumerate(trains):

    train['time'] = train['tms'].strftime('%H:%M')
    train['tms'] = train['tms'].isoformat()

    train['summary_text'] = f"{train['route']} {train['destination_city']} | {train['time']}"

    payload = json.dumps(train)

    logging.debug(payload)

    # Publish route to MQTT
    publish.single(args.mqtt_topic+'/route-'+str(idx), payload=payload, qos=0, retain=True, hostname=args.mqtt_host,
                   port=int(args.mqtt_port), client_id="DB-Routes", auth=mqtt_auth)
