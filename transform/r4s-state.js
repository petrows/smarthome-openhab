(function (dataString) {
    var data = JSON.parse(dataString);
    var state = data['state']

    if (0 == state) {
        return "OFF"
    }
    if (1 == state) {
        return "CFG"
    }
    if (2 == state) {
        return "ON"
    }
    if (4 == state) {
        return "WARM"
    }
    if (5 == state) {
        return "DELAY"
    }

    return "UNKNOWN"
})(input)
