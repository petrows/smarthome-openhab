// Function needs to convert from Raw Value to Using UoM
// https://www.openhab.org/docs/concepts/units-of-measurement.html

(function (dataString) {
    var data = JSON.parse(dataString);
    return data['humidity'] + ' %'
})(input)
