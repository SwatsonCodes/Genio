


$(document).ready(function() {
  $("p").hide();

  $('#search_button').click(function() {
  var load_icon = document.getElementById('load_animate');
  load_icon.className = "glyphicon glyphicon-refresh glyphicon-refresh-animate";
  $("p").show();
  var artist = $("#artist_input").val();
    $.ajax({
        type: "get",
        url: "http://localhost:9090/genio/",
        data: {'artist': artist},
        success: function(data) {
            if(data.related_artists.related_artists.length == 0){
                load_icon.className = "";
                alert("No related artists found on Rdio.");
                return;
            }
            localStorage.setItem('target_artist', JSON.stringify(artist));
            localStorage.setItem('related_artists', JSON.stringify(data));
            window.location.href ="http://localhost:9080/related-artists.html";
        },
        error: function(error) {
            console.log(error);
            load_icon.className = "";
            if(error.status == 500){
                alert("Could not find artist on Genius.");
            }
        }
    });
  });

  $("#artist_input").keyup(function(event){
    if(event.keyCode == 13){
        $("#search_button").click();
    }
  });

});