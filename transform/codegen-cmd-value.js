(function (input, field, transition, expire) {
    out = {}
    // Check: is number?
    if (isNaN(input)) {
        // Not a number
    } else {
        // Is a number
        input = Math.round(input)
    }
    // Write value
    out[field] = input
    // Write transition?
    if (transition && 0 != transition) {
        out['transition'] = Math.round(transition)
    }
    if (expire && 0 != expire && input == "ON") {
        out['on_time'] = Math.round(expire)
        // Add 'cooldown' f 1 seconds, as some device might require it
        out['off_wait_time'] = 1
    }
    return JSON.stringify(out)
})(input, f, t, exp)
