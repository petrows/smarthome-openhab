#!/bin/bash -xe

# Search instances
for instance_file in /srv/openhab-data/conf/codegen/devices/*.yaml; do
    instance_name=$(basename "$instance_file" .yaml)
    echo "Generating for $instance_name"
    z2m_root="/srv/zigbee2mqtt-data/$instance_name"
    if [ ! -d "$z2m_root" ]; then
        echo "Directory $z2m_root does not exist"
        exit 1
    fi

    mkdir -p "$z2m_root/devices-backup"

    cp "$z2m_root/devices.yaml" "$z2m_root/devices-backup/$(date +"%Y-%m-%d").yaml"
    cp "$instance_file" "$z2m_root/devices.yaml"

    docker restart Openhab-zigbee2mqtt-$instance_name
done

docker restart Openhab-yandex2mqtt
