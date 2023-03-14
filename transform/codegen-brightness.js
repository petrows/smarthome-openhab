(function(dataString) {
    var data = JSON.parse(dataString)
    return parseInt(data['brightness'])
})(input)
