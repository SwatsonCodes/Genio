$(document).ready(function() {
  $('#search_button').click(function() {
    $.ajax({
        type: "get",
        url: "http://localhost:9090/genio/",
        data: {'artist': 'busdriver'},
        success: function(data) {
            console.log(data);
        },
        error: function(error) {
            console.log(error);
        }
    });
  });

});