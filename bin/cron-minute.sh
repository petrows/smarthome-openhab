#!/bin/bash -e

ROOT_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

source "$ROOT_PATH/config.sh"

# Timetables broken since 2023
# # KVV timetable

# $ROOT_PATH/kvv-timetable.py --log=INFO --mqtt-host $MQTT_HOST --mqtt-port $MQTT_PORT --mqtt-user $MQTT_USER --mqtt-pass $MQTT_PASS --mqtt-topic kvv-timetable --stop-id $KVV_STOP_ID

# # DB timetable

# $ROOT_PATH/db-timetable.py --log=INFO --mqtt-host $MQTT_HOST --mqtt-port $MQTT_PORT --mqtt-user $MQTT_USER --mqtt-pass $MQTT_PASS --mqtt-topic db-timetable --stop-id $DB_STOP_ID --api-key $DB_API_KEY

