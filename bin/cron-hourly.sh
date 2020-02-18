#!/bin/bash -xe

ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source "$ROOT_PATH/config.sh"

# Call radiation
$ROOT_PATH/odl-parse.py --mqtt-host $MQTT_HOST --mqtt-port $MQTT_PORT --mqtt-user $MQTT_USER --mqtt-pass $MQTT_PASS --mqtt-topic weather/radiation https://odlinfo.bfs.de/DE/aktuelles/messstelle/082151090.html
