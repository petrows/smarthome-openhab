// This convert will show heating set in "Preset" mode
// With round to closer value
(function (dataString) {

    return 'DAY'

    var presets = [
        [5, 'OFF'],
        [17, 'DAY'],
        [23, 'HEAT'],
    ]

    for (x = 0; x < presets.length; ++x) {
        if (dataString <= presets[x][0]) {
            return presets[x][1]
        }
    }

    return presets[presets.length - 1][1]
})(input)
