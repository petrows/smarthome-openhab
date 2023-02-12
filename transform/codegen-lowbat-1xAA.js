(function(dataString) {
    var data = JSON.parse(dataString);

    if (data['voltage']) {
        var voltage = data['voltage'] / 1000.0

        if (voltage <= 1.0) {
            return "ON";
        }

        return "OFF";
    }

    throw new Error("No valid voltage found in '" + dataString + "'")
})(input)
