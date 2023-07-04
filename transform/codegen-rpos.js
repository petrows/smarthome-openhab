(function(dataString, channel) {
    var data = JSON.parse(dataString)
    var pos = parseInt(data[channel])
    return 100 - pos
})(input, channel)
