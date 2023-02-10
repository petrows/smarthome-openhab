// Send device mode -> controlled now

(function (x) {
    if (x == '1' || x == 'ON') {
        result = "{ \"system_mode\": \"heat\" }";
    } else {
        result = "{ \"system_mode\": \"off\" }";
    }
    return result;
})(input)
