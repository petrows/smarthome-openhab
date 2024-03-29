// Sample app to dump generated config for Yandex2mqtt device tree
// Run with: node bin/yandex2mqtt-dump.js
// or (better display): node bin/yandex2mqtt-dump.js | jq

// Allow to print full object
require('util').inspect.defaultOptions.depth = null;

const configDevices = require('../yandex2mqtt.devices');

console.log(JSON.stringify(configDevices));
