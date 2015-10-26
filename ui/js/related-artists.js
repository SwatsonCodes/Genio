$(document).ready(function() {

    window.onload = function() {
        document.getElementById('related_artists').innerHTML = localStorage.getItem('related_artists');
    }
});