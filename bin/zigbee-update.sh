#!/bin/bash

ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source "$ROOT_PATH/config.sh"

mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS -t 'zigbee2mqtt/bridge/request/device/ota_update/update' -m "{\"id\": \"$1\"}"
