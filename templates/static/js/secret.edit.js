
var map = null;
var geocoder = null;
var marker = null;
var localSearch = new GlocalSearch();

$('document').ready(function() {
  if (el = $('#id_title')) {
	el.focus();
  }
  if (GBrowserIsCompatible()) {
            canvas = document.getElementById("map_canvas");
    map = new GMap2(canvas);
    map.setCenter(new GLatLng(51.52487262675978, -0.1064300537109375), 15);
    map.addControl(new GLargeMapControl3D());
    marker = new GMarker(new GLatLng(51.52487262675978, -0.1064300537109375), {draggable: true});
    map.addOverlay(marker);
    GEvent.addListener(marker, "dragend", function() {
      point = marker.getPoint();
      document.getElementById('id_latitude').value = point.lat();
      document.getElementById('id_longitude').value = point.lng(); 
    });
    geocoder = new GClientGeocoder();
  }
  localSearch.setResultSetSize(google.search.Search.LARGE_RESULTSET);
  $('#id_title').blur(function() { if (!hasCoords()) { lookupAddress(); } });
  $('#id_title').keyup(function() { setLookupAddressTimeout(); });
  $('#id_location').blur(function() { if (!hasCoords()) { lookupAddress(); } });
});

function hasCoords() {
	return false; //$('#id_latitude').value || $('#id_longitude').value;
}

function getAddress() {
	return $('#id_title').val() + ' ' + $('#id_location').val();
}

var lookupAddressTimeout = null;
function setLookupAddressTimeout() {
	clearTimeout(lookupAddressTimeout);
	lookupAddressTimeout = setTimeout(lookupAddress, 1000);
}

function lookupAddress(address) {
	if (typeof(address) == 'undefined') {
		address = getAddress();
	}
	if (!jQuery.trim(address)) {
		return;
	}
  // first we try looking up using the google local ajax search API, which works better for postcodes

          localSearch.setSearchCompleteCallback(null,
      function() {
	clearTimeout(lookupAddressTimeout);
	if (localSearch.results[0]) {

		html = '';
		resultCount = localSearch.results.length;
		for (i = 0; i < resultCount; i++) {
			r = localSearch.results[i];
			html += '<li><a href="#" onclick="selectMapResult(' + r.lat + ',' + r.lng + ',\'' + r.titleNoFormatting.replace('\'', '\\\'') + '\',\'' + r.streetAddress.replace('\'', '\\\'') + '\'); return false;">' + r.title;
			if (r.streetAddress != r.title) { html += ', ' + r.streetAddress; }
			html += '</a></li>';
		}

		displayMapResults(html);
	
	} else {
		// if local search fails, we try the geocode address search

		if (geocoder) {
		    geocoder.getLatLng(
		      address + ', London',
		      function(point) {
			// we detect center of london as "no result"
			if (!point || ((point.lat() == 51.5001524) && (point.lng() == -0.1262362))) {
			  noMapResults();
			} else {
			  selectMapResult(point.lat(), point.lng());
			}
		      }
		    );
		  }
	}
              }
            );
          localSearch.execute(address + ', London');
}

function displayMapResults(listHtml) {
	document.getElementById('map_search_not_found').style.display = 'none';	
	document.getElementById('map_search_results_list').style.display = 'block';	
	results = document.getElementById('map_search_results_list');
	results.innerHTML = listHtml;
}

function noMapResults() {
	document.getElementById('map_search_not_found').style.display = 'block';	
	document.getElementById('map_search_results_list').style.display = 'none';	
}

function selectMapResult(lat, lng, title, address) {
	document.getElementById('map_search_not_found').style.display = 'none';	
	document.getElementById('map_search_results_list').style.display = 'none';
  	document.getElementById('id_latitude').value = lat;
  	document.getElementById('id_longitude').value = lng;
	map.setCenter(new GLatLng(lat, lng), 15);
	if (marker) {
	    marker.setLatLng(new GLatLng(lat, lng));
	}
	// we use settimeout to give the map time to render before we pop up the dialog
	setTimeout(function() {
		titleField = $('#id_title');
		if (title && (title != titleField.val()) && (!titleField.val() || confirm('Update title field to "' + title + '"?'))) {
			titleField.val(title);
		}
		locationField = $('#id_location');
		if (address && (address != locationField.val()) && (!locationField.val() || confirm('Update location field to "' + address + '"?'))) {
			locationField.val(address);
		}
	}, 200);
}
