(function (dataString) {
    var data = JSON.parse(dataString);
    var h = data['hours']
    var m = data['mins']
    return h + ":" + (m < 10 ? '0' : '') + m
})(input)
