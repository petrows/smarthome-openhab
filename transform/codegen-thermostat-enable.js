// Default mode - using `system_mode` channel

(function(dataString) {
    var data = JSON.parse(dataString);
    var system_mode = data['system_mode'];
    if (system_mode == 'off') {
        return "OFF";
    }
    return "ON";
})(input)
