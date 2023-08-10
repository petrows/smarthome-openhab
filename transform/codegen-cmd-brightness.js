(function (input, transition) {
    out = {
        'brightness': Math.round(input),
        'transition': transition,
    }
    return JSON.stringify(out)
})(input, transition)
