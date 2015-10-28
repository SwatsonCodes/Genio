$(document).ready(function() {

  $('#search_button').click(function() {
  var artist = $("#artist_input").val();
    $.ajax({
        type: "get",
        url: "http://localhost:9090/genio/",
        data: {'artist': artist},
        success: function(data) {
            localStorage.setItem('target_artist', JSON.stringify(artist));
            localStorage.setItem('related_artists', JSON.stringify(data));
            window.location.href ="http://localhost:9080/related-artists.html";
        },
        error: function(error) {
            console.log(error);
        }
    });
  });

});