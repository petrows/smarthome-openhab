(function (dataString) {
    // Dsiplay MIRED color temp in K
    mired = 150 + (500 - 150) * (dataString / 100)
    kelvin = Math.round(1000000.0 / mired)
    return kelvin + "K"
})(input)
