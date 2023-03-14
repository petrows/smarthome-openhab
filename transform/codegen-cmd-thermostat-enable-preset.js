// Switch thermostat using `preset` channel
// manual - operational
// holiday - disabled

(function(x) {
    preset = 'holiday'
    if (x == '1' || x == 'ON') {
        preset = 'manual'
    }
    cmd = { preset: preset }
    return JSON.stringify(cmd)
})(input)
