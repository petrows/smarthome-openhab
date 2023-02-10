// Function controls the Zigbee Valve Thermostat
// Devices, which have "Preset"

(function (x) {
    x = parseFloat(x)

    if (x < 5) { x = 5 }
    if (x > 30) { x = 30 }

    preset = "heat"

    result = "{ \"system_mode\": \"" + preset + "\", \"current_heating_setpoint\": " + x + " }";

    return result;
})(input)
