(function(x) {
    system_mode = 'off'
    if (x == '1' || x == 'ON') {
        system_mode = 'heat'
    }
    cmd = { system_mode: system_mode }
    return JSON.stringify(cmd)
})(input)
