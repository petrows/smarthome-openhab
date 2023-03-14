// Thermostat does not have built-in on/off modes,
// use 5°C setting as on/off toggle

(function(dataString) {
    var data = JSON.parse(dataString);
    var temp = parseInt(data['current_heating_setpoint'])
    if (temp <= 5) {
        return "OFF";
    }
    return "ON";
})(input)
