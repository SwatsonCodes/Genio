$(document).ready(function() {

  $('#search_button').click(function() {
  var artist = $("#artist_input").val();
    $.ajax({
        type: "get",
        url: "http://localhost:9090/genio/",
        data: {'artist': artist},
        success: function(data) {
            console.log(data);
        },
        error: function(error) {
            console.log(error);
        }
    });
  });

});