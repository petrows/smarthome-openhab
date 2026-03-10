#!/bin/bash
# Script to reset Kajplats by toggling the state 12 times via MQTT (Non-filament!)

set -euo pipefail

usage() {
	echo "Usage: $0 --host <mqtt-host> --topic <z2m-topic>/set [--port <port>] [--username <user>] [--password <pass>] [--qos <0|1|2>] [--retain]"
	exit 1
}

HOST=""
TOPIC=""
PORT="1883"
USERNAME=""
PASSWORD=""
QOS="0"
RETAIN="false"

while [[ $# -gt 0 ]]; do
	case "$1" in
		--host)
			HOST="${2:-}"
			shift 2
			;;
		--topic)
			TOPIC="${2:-}"
			shift 2
			;;
		--port)
			PORT="${2:-}"
			shift 2
			;;
		--username)
			USERNAME="${2:-}"
			shift 2
			;;
		--password)
			PASSWORD="${2:-}"
			shift 2
			;;
		--qos)
			QOS="${2:-}"
			shift 2
			;;
		--retain)
			RETAIN="true"
			shift
			;;
		-h|--help)
			usage
			;;
		*)
			echo "Unknown argument: $1"
			usage
			;;
	esac
done

[[ -z "$HOST" || -z "$TOPIC" ]] && usage

if ! command -v mosquitto_pub >/dev/null 2>&1; then
	echo "Error: mosquitto_pub is required but not installed."
	exit 1
fi

PUB_ARGS=(-h "$HOST" -p "$PORT" -t "$TOPIC" -q "$QOS")
[[ "$RETAIN" == "true" ]] && PUB_ARGS+=( -r )
[[ -n "$USERNAME" ]] && PUB_ARGS+=( -u "$USERNAME" )
[[ -n "$PASSWORD" ]] && PUB_ARGS+=( -P "$PASSWORD" )

for _ in {1..12}; do
	mosquitto_pub "${PUB_ARGS[@]}" -m '{"state":"OFF"}'
	sleep 1
	mosquitto_pub "${PUB_ARGS[@]}" -m '{"state":"ON"}'
	sleep 1
done

