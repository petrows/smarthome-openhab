(function (dataString) {
    var data = JSON.parse(dataString);

    if (data['temperature']) {
        return data['temperature']
    }

    if (data['local_temperature']) {
        return data['local_temperature']
    }

    throw new Error("No valid temperature found in '" + dataString + "'")
})(input)
