(function (x, channel) {
    var v = Math.round(x)
    v = 100 - v
    return "{\"" + channel + "\":" + v + "}"
})(input, channel)
