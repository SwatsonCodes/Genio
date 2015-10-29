// portions of this code and associated html were taken from the open source Rdio hello-web-playback example
// https://github.com/rdio/hello-web-playback

// a global variable that will hold a reference to the api swf once it has loaded
var apiswf = null;

$(document).ready(function() {
  // on page load use SWFObject to load the API swf into div#apiswf
  var flashvars = {
    'playbackToken': playback_token, // from token.js
    'domain': domain,                // from token.js
    'listener': 'callback_object'    // the global name of the object that will receive callbacks from the SWF
    };
  var params = {
    'allowScriptAccess': 'always'
  };
  var attributes = {};
  swfobject.embedSWF('http://www.rdio.com/api/swf/', // the location of the Rdio Playback API SWF
      'apiswf', // the ID of the element that will be replaced with the SWF
      1, 1, '9.0.0', 'expressInstall.swf', flashvars, params, attributes);

  //search box
  $('#search_button').click(function() {
  var load_icon = document.getElementById('load_animate');
  load_icon.className = "glyphicon glyphicon-refresh glyphicon-refresh-animate";
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

  // show target artist name
  document.getElementById('target_artist').insertAdjacentHTML('beforeend', JSON.parse(localStorage.getItem('target_artist')) + ': ');

  // show related artists
  var artist_data = JSON.parse(localStorage.getItem('related_artists')).related_artists;
  var artist_names = artist_data.related_artists;
  var artist_images = artist_data.artist_images;
  var radio_keys = artist_data.radio_keys;
  var fragments = artist_data.fragments;

  function load_related_artist(index) {
      var related_artist = document.createElement("a");
      related_artist.className = "list-group-item";
      var play_button = document.createElement("BUTTON");
      play_button.className = "btn btn-default"
      play_button.onclick = function() {
          apiswf.rdio_play(radio_keys[index]);
      };
      var play_icon = document.createElement("I");
      play_icon.className = "fa fa-play-circle";
      play_button.appendChild(play_icon);
      related_artist.appendChild(play_button)
      var artist_icon = document.createElement("IMG");
      artist_icon.src = artist_images[index];
      related_artist.appendChild(artist_icon);
      related_artist.appendChild(document.createTextNode(artist_names[index]));
      var fragment = document.createElement("EM");
      fragment.appendChild(document.createTextNode(fragments[index]));
      related_artist.appendChild(fragment);
      document.getElementById("artist-list").appendChild(related_artist);
  }

  var num_results = Math.min(artist_names.length, 10);
  for(i=0;i<num_results;i++){
    load_related_artist(i)
  }


  // set up the controls
  $('#play').click(function() { apiswf.rdio_play(); });
  $('#stop').click(function() { apiswf.rdio_stop(); });
  $('#pause').click(function() { apiswf.rdio_pause(); });
  $('#previous').click(function() { apiswf.rdio_previous(); });
  $('#next').click(function() { apiswf.rdio_next(); });
});


// the global callback object
var callback_object = {};

callback_object.ready = function ready(user) {
  // Called once the API SWF has loaded and is ready to accept method calls.

  // find the embed/object element
  apiswf = $('#apiswf').get(0);

  apiswf.rdio_startFrequencyAnalyzer({
    frequencies: '10-band',
    period: 100
  });
}

callback_object.freeRemainingChanged = function freeRemainingChanged(remaining) {
  $('#remaining').text(remaining);
}

callback_object.playingTrackChanged = function playingTrackChanged(playingTrack, sourcePosition) {
  // The currently playing track has changed.
  // Track metadata is provided as playingTrack and the position within the playing source as sourcePosition.
  if (playingTrack != null) {
    $('#track').text(playingTrack['name']);
    $('#album').text(playingTrack['album']);
    $('#artist').text(playingTrack['artist']);
    $('#art').attr('src', playingTrack['icon']);
  }
}

callback_object.playingSourceChanged = function playingSourceChanged(playingSource) {
  // The currently playing source changed.
  // The source metadata, including a track listing is inside playingSource.
}

callback_object.volumeChanged = function volumeChanged(volume) {
  // The volume changed to volume, a number between 0 and 1.
}

callback_object.muteChanged = function muteChanged(mute) {
  // Mute was changed. mute will either be true (for muting enabled) or false (for muting disabled).
}


callback_object.queueChanged = function queueChanged(newQueue) {
  // The queue has changed to newQueue.
}

callback_object.shuffleChanged = function shuffleChanged(shuffle) {
  // The shuffle mode has changed.
  // shuffle is a boolean, true for shuffle, false for normal playback order.
}

callback_object.repeatChanged = function repeatChanged(repeatMode) {
  // The repeat mode change.
  // repeatMode will be one of: 0: no-repeat, 1: track-repeat or 2: whole-source-repeat.
}

callback_object.playingSomewhereElse = function playingSomewhereElse() {
  // An Rdio user can only play from one location at a time.
  // If playback begins somewhere else then playback will stop and this callback will be called.
}

callback_object.updateFrequencyData = function updateFrequencyData(arrayAsString) {
  // Called with frequency information after apiswf.rdio_startFrequencyAnalyzer(options) is called.
  // arrayAsString is a list of comma separated floats.

  var arr = arrayAsString.split(',');

  $('#freq div').each(function(i) {
    $(this).width(parseInt(parseFloat(arr[i])*500));
  })
}

