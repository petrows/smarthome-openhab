#!/bin/bash -xe

# This script applies devices list to Zigbee2mqtt and reloads it

mkdir -p /srv/zigbee2mqtt-data/devices-backup

cp /srv/zigbee2mqtt-data/devices.yaml /srv/zigbee2mqtt-data/devices-backup/$(date +"%Y-%m-%d").yaml
cp /srv/openhab-data/conf/devices.yaml /srv/zigbee2mqtt-data/

docker restart Openhab-zigbee2mqtt
docker restart Openhab-yandex2mqtt
