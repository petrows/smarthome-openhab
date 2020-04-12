#!/usr/bin/env python3

from lxml import html
import paho.mqtt.publish as publish
import requests
import argparse

rad_level = 0.0136

parser = argparse.ArgumentParser(description='Parse radiation level')

parser.add_argument('url', metavar='URL', type=str,
                    help='URL to the odlinfo.bfs.de page, e.q. https://odlinfo.bfs.de/DE/aktuelles/messstelle/082151090.html')

parser.add_argument('--mqtt-host', help='MQTT broker host')
parser.add_argument('--mqtt-port', help='MQTT broker port')
parser.add_argument('--mqtt-user', help='MQTT broker user')
parser.add_argument('--mqtt-pass', help='MQTT broker password')
parser.add_argument('--mqtt-topic', help='MQTT broker topic')

args = parser.parse_args()

print(args)

mqtt_auth = {'username':args.mqtt_user, 'password':args.mqtt_pass}

page = requests.get(args.url)
tree = html.fromstring(page.content)

mes = tree.xpath('//p[@class="aktmw"]/strong/text()')
mes = mes[0]
mes = mes.split(' ')
mes = mes[0]
mes = mes.replace(',','.')

mes = float(mes)

print("Current value is: %f" % mes)

publish.single(args.mqtt_topic, payload=mes, qos=0, retain=True, hostname=args.mqtt_host,
    port=int(args.mqtt_port), client_id="WeatherRadiationMeter", auth=mqtt_auth)
