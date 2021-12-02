(function (dataString) {
    var data = JSON.parse(dataString);
    if (data['IRSend'] == "Done") {
        return "OFF"
    }
})(input)
