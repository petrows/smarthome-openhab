(function (dataString) {
    var data = JSON.parse(dataString);

    if (data['voltage']) {
        return data['voltage'] / 1000.0
    }

    throw new Error("No valid voltage found in '" + dataString + "'")
})(input)
