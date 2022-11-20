#!/bin/bash -xe

# This script applies devices list to Zigbee2mqtt and reloads it

cp /srv/zigbee2mqtt-data/devices.yaml /srv/zigbee2mqtt-data/devices-$(date +"%Y-%m-%d").yaml
cp /srv/openhab-data/conf/devices.yaml /srv/zigbee2mqtt-data/

docker restart Openhab-zigbee2mqtt
