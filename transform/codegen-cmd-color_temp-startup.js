// This file sets CT option to devices, who can configure pre-startup
(function(x) {
    var v = Math.round(x)
    cmd = { color_temp: v, color_temp_startup: v, transition: 3 }
    return JSON.stringify(cmd)
})(input)
