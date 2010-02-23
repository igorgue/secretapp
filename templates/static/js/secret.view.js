var createMap = function(lat, lng, map_selector){
    var latlng = new GLatLng(lat, lng);
    var google_map = $(map_selector);
    
    // create map if it doesn't exist
    google_map.show();
    map = new GMap2(google_map[0]);
    map.addControl(new GLargeMapControl3D());
    // set the center
    map.setCenter(latlng, 15);
    map.addOverlay(new GMarker(latlng, {draggable: true}));
}


$(document).ready(function(){
    $('#id_secretcomment #id_text').defaultText('Leave a comment here!');
});