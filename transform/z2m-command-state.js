(function(x) {
    var result = "";
    if (x == '1' || x == 'ON') {
        result="{ \"state\": \"ON\", \"transition\": 1 }";
    } else {
        result = "{ \"state\": \"OFF\", \"transition\": 1 }";
    }
    return result;
})(input)
