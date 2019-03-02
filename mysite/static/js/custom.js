function initMap(){
  var options = {
    zoom: 11,
    center: {lat:43.012960,lng:-83.712583}
  }

  var map = new google.maps.Map(document.getElementById('map'), options);
}
