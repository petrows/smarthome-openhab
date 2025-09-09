// Args:
// f = field name
// t = transition time (seconds) (optional)
// exp = expire time (seconds) (optional, only for ON command, max 6553 seconds)

(function (input) {
    out = {}
    // Check: is number?
    if (isNaN(input)) {
        // Not a number
    } else {
        // Is a number
        input = Math.round(input)
    }
    // Write value
    out[f] = input
    // Write transition?
    if (t && 0 != t) {
        out['transition'] = Math.round(t)
    }
    if (exp && 0 != exp && exp <= 6553 && input == "ON") {
        out['on_time'] = Math.round(exp)
        // Add 'cooldown' f 1 seconds, as some device might require it
        out['off_wait_time'] = 1
    }
    return JSON.stringify(out)
})(input)
