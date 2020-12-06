(function (dataString) {
    // Make a fuzzy time
    // https://stackoverflow.com/a/7641812

    var delta = Math.round((+new Date - new Date(dataString)) / 1000);

    if (isNaN(delta)) {
        return "?"
    }

    var minute = 60,
        hour = minute * 60,
        day = hour * 24,
        week = day * 7;

    var fuzzy;

    if (delta < 30) {
        fuzzy = 'Now';
    } else if (delta < minute) {
        fuzzy = delta + ' s';
    } else if (delta < hour) {
        fuzzy = Math.floor(delta / minute) + ' m';
    } else if (delta < day) {
        fuzzy = Math.floor(delta / hour) + ' h';
    } else {
        fuzzy = Math.floor(delta / day) + ' d';
    }

    return fuzzy;
})(input)
