(function(dataString) {
    var data = JSON.parse(dataString);
    var batt = data['battery'];

    if (batt <= 20) {
        return "ON";
    }

    return "OFF";
})(input)