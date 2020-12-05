(function (dataString) {
    var data = JSON.parse(dataString);
    var val = data['occupancy'];

    if (val) {
        return "ON";
    }

    return "OFF";
})(input)
