(function(x) {
    var result = "";
    if (x == '1' || x == 'ON') {
        result="{ \"state\": \"ON\" }";
    } else {
        result = "{ \"state\": \"OFF\" }";
    }
    return result;
})(input)
