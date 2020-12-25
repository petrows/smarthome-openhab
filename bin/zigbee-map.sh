#!/bin/bash

# additional dependencies: graphviz imagemagick

# put temporal files in ram filesystem
file="/tmp/networkmap"
fechahora=$(date '+%F-%H:%M')
#~ echo $fechahora

ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source "$ROOT_PATH/config.sh"

mosquitto_sub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS -t zigbee2mqtt/bridge/networkmap/graphviz -C 1 >${file}.dot &
mosquitto_pub -h $MQTT_HOST -u $MQTT_USER -P $MQTT_PASS -t zigbee2mqtt/bridge/networkmap/routes -m graphviz

# wait until mosquitto_sub ends
wait

# generate graphic with graphviz (change to short texts with sed)
cat ${file}.dot|sed -e 's/Xiaomi Aqara temperature, humidity and pressure sensor/AqaraTHP/g'|sed -e 's/Xiaomi Mi\/Aqara smart home cube/AqaraCube/g'|sed -e 's/Xiaomi Aqaradouble key wireless wall switch/AqaraDoubleSwitch/g'|circo -Tsvg  > ${fechahora}.svg

# display with imageMagick command
# display ${file}${fechahora}.svg &
echo "File: ${fechahora}.svg"
