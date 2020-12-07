(function(x) {
    var result = "";
    if (x == '1' || x == 'ON') {
        result="{ \"state\": \"ON\" }";
    } else {
        result = "{ \"state\": \"OFF\", \"transition\": 2 }";
    }
    return result;
})(input)
