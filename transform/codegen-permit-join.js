(function(dataString) {
    var data = JSON.parse(dataString);
    var permit = data['permit_join'];

    if (permit) {
        return "ON";
    }

    return "OFF";
})(input)
