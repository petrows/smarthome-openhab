// Filter value and clean logs

(function (dataString) {
    var data = JSON.parse(dataString);
    var value = data['action'];
    return value;
})(input)
