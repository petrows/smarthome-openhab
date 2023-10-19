(function (input, field, transition) {
    out = {}
    input = parseFloat(input)
    out[field] = input
    return JSON.stringify(out)
})(input, f)
