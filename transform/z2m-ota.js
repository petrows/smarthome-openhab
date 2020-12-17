(function (dataString) {
    var data = JSON.parse(dataString);
    var ota = data['update_available'];
    return ota ? "ON" : "OFF"
})(input)
