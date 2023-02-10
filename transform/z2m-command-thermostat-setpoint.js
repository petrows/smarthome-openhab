// Function controls the Zigbee Valve Thermostat
// For devices, which does not have "preset"

(function (x) {
    x = parseFloat(x)

    if (x < 5) { x = 5 }
    if (x > 30) { x = 30 }

    result = "{ \"current_heating_setpoint\": " + x + " }";

    return result;
})(input)
