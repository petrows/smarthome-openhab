(function (input, field, transition) {
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
    return JSON.stringify(out)
})(input, f, t)
