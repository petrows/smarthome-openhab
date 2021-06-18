// Function controls the Zigbee Valve Thermostat

(function (x) {
    x = parseFloat(x)

    if (x < 5) { x = 5 }
    if (x > 30) { x = 30 }

    mode = "auto"
    if (x == 5) { mode = "off" }

    result = "{ \"preset\": \"manual\", \"system_mode\": \"" + mode + "\", \"current_heating_setpoint\": " + x + " }";
    //result = "{ \"current_heating_setpoint\": " + x + " }";

    return result;
})(input)
