// Default mode - using `preset` channel

(function(dataString) {
    var data = JSON.parse(dataString);
    var system_mode = data['preset'];
    if (system_mode == 'holiday') {
        return "OFF";
    }
    return "ON";
})(input)
