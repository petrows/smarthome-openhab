(function(dataString) {
    var data = JSON.parse(dataString);
    var batt = data['battery'];

    if (batt <= 10) {
        return "ON";
    }

    return "OFF";
})(input)
