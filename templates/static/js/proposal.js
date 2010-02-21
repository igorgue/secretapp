$(document).ready(function() {
	$('.suggest_tab_button').each(function(index) {
		$(this).click(function() {
			var df = $(this).closest('.discussion_reply_form');
			df.removeClass('comment').toggleClass('suggest');
			//if (df.hasClass('suggest')) { df.find('.secret_name').focus(); }
			return false;
		});
	});
	$('.comment_tab_button').each(function(index) {
		$(this).click(function() {
			var df = $(this).closest('.discussion_reply_form');
			df.removeClass('suggest').toggleClass('comment');
			if (df.hasClass('comment')) { df.find('textarea.comment').focus(); }
			return false;
		});
	});
});

var secretListController = {
	parentElement : null,
	map : null,
	map_small : null,
	geocoder : null,
	marker : null,
	marker_small : null,
	localSearch : new GlocalSearch(),

	title_hinttext : 'Name of this secret',
	location_hinttext : 'Location',
	
	hasInit : false,
	init : function(parentElement) {
		if (this.hasInit) { return; }
		this.hasInit = true;
		this.parentElement = parentElement;
		
		this.geocoder = new GClientGeocoder();
		this.localSearch.setResultSetSize(google.search.Search.LARGE_RESULTSET);

		secret = this.addSecret();
		parentElement.find('.add_secret a').each(function() {
			$(this).click(function() { secretListController.addSecret(); });
		});
		parentElement.find('.cancel').each(function() {
			$(this).click(function() {
				var df = $(this).closest('.discussion_reply_form');
				df.removeClass('suggest').removeClass('comment');
			 });
		});
		
		parentElement.submit(function() { secretListController.submitHandler(); return false; });
	},

	hasInitMaps : false,
	initMaps : function() {
		if (this.hasInitMaps) { return true; }
		// map must be visible before we can init it else bad things happen(tm)
		if (!this.mapVisible()) { return false; }
		this.hasInitMaps = true;
		if (GBrowserIsCompatible()) {
			canvas = this.parentElement.find('.map_canvas')[0];
			this.map = new GMap2(canvas);
			this.map.setCenter(new GLatLng(51.52487262675978, -0.1064300537109375), 15);
			this.map.addControl(new GLargeMapControl3D());
			this.marker = new GMarker(new GLatLng(51.52487262675978, -0.1064300537109375), {draggable: true});
			this.map.addOverlay(this.marker);
			var this2 = this;
			GEvent.addListener(this.marker, "dragend", function() {
				point = this2.marker.getPoint();
				this2.saveNewMarkerPosition(point);
				this2.updateMapMarkerPosition(point);
			});

			canvas_small = this.parentElement.find('.map_canvas_small')[0];
			this.map_small = new GMap2(canvas_small);
			this.map_small.disableDragging();
			this.map_small.setCenter(new GLatLng(51.52487262675978, -0.1064300537109375), 13);
			this.marker_small = new GMarker(new GLatLng(51.52487262675978, -0.1064300537109375));
			this.map_small.addOverlay(this.marker_small);
		}
	},

	mapVisible : function() {
		return this.parentElement.hasClass('suggest') && this.parentElement.find('.bigmap')[0];
	},

	getExpandedSecretLI : function() {
		return this.parentElement.find('.secrets_list li.secret.expanded'); // .first()??
	},
	
	getAddress : function() {
		var title = this.parentElement.find('.expanded .secret_name').val();
		var location = this.parentElement.find('.expanded .secret_location').val();
		if (title == this.title_hinttext) { title = ''; }
		if (location == this.location_hinttext) { location = ''; }
		return title + ' ' + location;
	},
	
	hasCoords : function() {
		return false; //$('#id_latitude').value || $('#id_longitude').value;
	},
	
	lookupAddressTimeout : null,
	setLookupAddressTimeout : function() {
		clearTimeout(this.lookupAddressTimeout);
		this.lookupAddressTimeout = setTimeout(this.lookupAddress, 1000);
	},
	
	lookupAddress : function(address) {
		if (typeof(address) == 'undefined') {
			address = this.getAddress();
		}
		if (!jQuery.trim(address)) {
			return;
		}
		// first we try looking up using the google local ajax search API, which works better for postcodes
	
		this.localSearch.setSearchCompleteCallback(null, function() { secretListController.searchCompleteCallback(address); });
		this.localSearch.execute(address + ', London');
	},
	
	searchCompleteCallback : function(address) {
		clearTimeout(this.lookupAddressTimeout);
		var html = '';
		if (this.localSearch.results[0]) {
			var lat;
			var lng;
			resultCount = this.localSearch.results.length;
			for (i = 0; i < resultCount; i++) {
				r = this.localSearch.results[i];
				lat = r.lat;
				lng = r.lng;
				html += '<li><a href="#" onclick="secretListController.selectMapResult(' + r.lat + ',' + r.lng + ',\'' + r.titleNoFormatting.replace('\'', '\\\'') + '\',\'' + r.streetAddress.replace('\'', '\\\'') + '\'); return false;">' + r.title;
				if (r.streetAddress != r.title) { html += ', ' + r.streetAddress; }
				html += '</a></li>';
			}
			if (resultCount == 1) {
				this.displayMapResults(html, new GLatLng(lat, lng));
			} else {
				this.displayMapResults(html);
			}
		} else {
			// if local search fails, we try the geocode address search
			if (this.geocoder) {
			    this.geocoder.getLatLng(
			      address + ', London',
			      function(point) {
					// we detect center of london as "no result"
					if (!point || ((point.lat() == 51.5001524) && (point.lng() == -0.1262362))) {
					  secretListController.noMapResults();
					} else {
						html += '<li><a href="#" onclick="secretListController.selectMapResult(' + point.lat() + ',' + point.lng() + ',\'' + address.replace('\'', '\\\'') + '\',\'' + '\'); return false;">' + r.title;
						if (r.streetAddress != r.title) { html += ', ' + r.streetAddress; }
						html += '</a></li>';
						secretListController.displayMapResults(html, point);
					}
				  }
				);
			}
		}
    },

	
	displayMapResults : function(listHtml, point) {
		this.parentElement.find('.map_search_not_found')[0].style.display = 'none';	
		this.parentElement.find('.map_search_results_list')[0].style.display = 'block';	
		results = this.parentElement.find('.map_search_results_list ol')[0];
		results.innerHTML = listHtml;
		if (point && !this.currentSecretHasMarker()) {
			this.getExpandedSecretLI().addClass('bigmap');
			this.saveNewMarkerPosition(point);
		} else {
			this.updateMapMarkerPosition();
		}
	},
	
	noMapResults: function() {
		this.parentElement.find('.map_search_not_found')[0].style.display = 'block';	
		this.parentElement.find('.map_search_results_list')[0].style.display = 'none';	
		this.getExpandedSecretLI().removeClass('bigmap');
	},
	
	clearMapResults: function() {
		this.parentElement.find('.map_search_not_found')[0].style.display = 'none';	
		this.parentElement.find('.map_search_results_list')[0].style.display = 'none';	
		this.getExpandedSecretLI().removeClass('bigmap');
	},
	
	selectMapResult : function(lat, lng, title, address) {
		this.parentElement.find('.map_search_not_found')[0].style.display = 'none';	
		this.parentElement.find('.map_search_results_list')[0].style.display = 'none';
		this.getExpandedSecretLI().addClass('bigmap');
		this.initMaps();
		point = new GLatLng(lat, lng);
		if (this.marker) {
		    this.marker.setLatLng(point);
		}
		this.saveNewMarkerPosition(point);
		// we use settimeout to give the map time to render before we pop up the dialog
		setTimeout(function() { secretListController.updateTitleAndLocation(title, address); }, 200);
	},
	
	saveNewMarkerPosition : function(point) {
	  	expandedSecret = this.getExpandedSecretLI();
		expandedSecret.find('.latitude')[0].value = point.lat();
		expandedSecret.find('.longitude')[0].value = point.lng(); 
	  	if (point.lat() && point.lng()) {
	  		expandedSecret.addClass('hasmap');
			this.initMaps();
			point2 = new GLatLng(point.lat(), point.lng());
			this.map.setCenter(point2, 15);
			this.map_small.setCenter(point2, 13);
			if (this.marker) {
			    this.marker.setLatLng(point);
			}
			if (this.marker_small) {
			    this.marker_small.setLatLng(point);
			}
	  	}
	},
	
	updateMapMarkerPosition : function() {
	  	expandedSecret = this.getExpandedSecretLI();
		lat = expandedSecret.find('.latitude').val();
		lng = expandedSecret.find('.longitude').val();
		if (lat && lng) { 
			point = new GLatLng(lat, lng);
			if (this.initMaps()) {
				this.map.setCenter(point, 15);
				this.map_small.setCenter(point, 13);
				if (this.marker) {
				    this.marker.setLatLng(point);
				}
				if (this.marker_small) {
				    this.marker_small.setLatLng(point);
				}
			}
		} else {
			// we have no position - re-center
			lat = 51.5001524;
			lng = -0.1262362;
			point = new GLatLng(lat, lng);
			if (this.initMaps()) {
				this.map.setCenter(point, 15);
				this.map_small.setCenter(point, 13);
				// hide marker somewhere random
				point = new GLatLng(0, 0);
				if (this.marker) {
				    this.marker.setLatLng(point);
				}
				if (this.marker_small) {
				    this.marker_small.setLatLng(point);
				}
			}
		}
	},

	currentSecretHasMarker : function() {
	  	expandedSecret = this.getExpandedSecretLI();
		lat = expandedSecret.find('.latitude').val();
		lng = expandedSecret.find('.longitude').val();
		return lat || lng;
	},

	updateTitleAndLocation : function(title, address) {
		expandedSecret = this.getExpandedSecretLI();
        titleField = expandedSecret.find('.secret_name');
		if (title && (title != titleField.val()) && (!titleField.val() || titleField.val() == this.title_hinttext || true || confirm('Update title field to "' + title + '"?'))) {
			titleField.val(title);
			titleField.triggerHandler('change');
		}
		locationField = expandedSecret.find('.secret_location');
		if (address && (address != locationField.val()) && (!locationField.val() || (locationField.val() == this.location_hinttext) || true || confirm('Update location field to "' + address + '"?'))) {
			locationField.val(address);
			locationField.triggerHandler('change');
		}
	},
	
	
	//
	// secrets list
	//
	
	secret_template : '\
	<li class="secret expanded" id="secret-__id__">\
		<div class="edit">\
			<label for="id_title-__id__" class="secret_name_label">Name of this secret</label>\
			<input id="id_title-__id__" type="text" name="" value="" class="secret_name"/>\
			<label for="id_location-__id__" class="secret_location_label">Location</label>\
			<input id="id_location-__id__" type="text" name="" value="" class="secret_location"/>\
			<br class="clear_left" />\
			<a href="#" class="find_on_map_button pink_button">Find on map</a>\
			<a href="#" class="edit_map_button pink_button">Edit map</a>\
			<a href="#" class="hide_map_button pink_button">Hide map</a>\
		</div>\
		\
		<div class="static">\
			<span class="title">New secret</span>\
			<span class="location"> - </span>\
		</div>\
		\
		<input type="hidden" name="latitude" id="id_latitude-__id__" class="hidden latitude" value="">\
		<input type="hidden" name="longitude" id="id_longitude-__id__" class="hidden longitude" value="">\
		<input type="hidden" name="secret_pk" id="id_secret_pk-__id__" class="hidden pk" value="">\
		\
		<input type="image" src="http://media.groupspaces.com/images/icons/silk/cross.png" class="delete_button" />\
		<br style="clear: both;" />\
	</li>\
	',
	
	secret_count : 0,
	
	addSecret : function() {
		this.collapseAllSecrets();
		new_secret = this.secret_template;
		new_secret = new_secret.replace(/__id__/g, this.secret_count);
		this.parentElement.find('.secrets_list').append(new_secret);
		new_secret = $('#secret-' + this.secret_count);
		this.initSecret(new_secret, this.secret_count);
		this.expandSecret(new_secret);
		//new_secret.find('.secret_name').focus();
		this.secret_count++;
		return new_secret;
	},
	
	initSecret : function(li, id_key) {
		li = $(li);
		li.find('.static').click(function() {
			secretListController.expandSecret(this);
		});
		li.find('.find_on_map_button').click(function() {
			secretListController.lookupAddress();
			return false;
		});
		li.find('.edit_map_button').click(function() {
			secretListController.getExpandedSecretLI().addClass('bigmap');
			return false;
		});
		li.find('.hide_map_button').click(function() {
			secretListController.getExpandedSecretLI().removeClass('bigmap');
			return false;
		});
		li.find('.delete_button').click(function() {
			secretListController.deleteSecret(this);
		});
 		li.find('.secret_name').change(function() {
				var title = $(this).val();
				if (!title) { title = 'New Secret'; }
				li.find('.static .title').text(title);
			}).blur(function() {
				if (!secretListController.hasCoords()) { secretListController.lookupAddress(); }
			}).keyup(function() {
				secretListController.setLookupAddressTimeout();
			});
		
		li.find('.secret_location').change(function() {
				var loc = $(this).val();
				if (!loc) { loc = ' - '; }
				li.find('.static .location').text(loc);
			}).blur(function() {
				if (!secretListController.hasCoords()) { secretListController.lookupAddress(); }
			});
		configTextBoxPrompt($('#id_title-' + id_key), this.title_hinttext);
		configTextBoxPrompt($('#id_location-' + id_key), this.location_hinttext);
	},
	
	collapseAllSecrets : function() {
		this.parentElement.find('.secrets_list li.secret').each(function() {
			$(this).removeClass('expanded');
		});
	},
	
	expandSecret : function(el) {
		secret_li = $(el).closest('li.secret');
		this.collapseAllSecrets();
		if (m = this.parentElement.find('.suggest_secret').children('.map')) {
			secret_li.append(m);
		}
		secret_li.addClass('expanded');
		secret_li.append(secret_li.parent().find('.map'));
		this.clearMapResults();
		this.updateMapMarkerPosition();
	},
	
	deleteSecret : function(el) {
		var el = $(el).closest('li.secret');
		if (m = $(el).find('.map')) {
			this.parentElement.find('.suggest_secret').append(m);
		}
		$(el).remove();
	},
	
	submitHandler : function() {
		secrets = [];
		this.parentElement.find('.ajax_in_progress').css('display','block');
		if (this.parentElement.hasClass('suggest')) {
			this.parentElement.find('.secrets_list').children().each(function() {
				var secret = $(this);
				$.ajax({
				  type: 'POST',
				  url: '/secret/new_discussion/',
				  data: {title: secret.find('input.secret_name').val(), location: secret.find('input.secret_location').val(), latitude: secret.find('input.latitude').val(), longitude: secret.find('input.longitude').val()},
				  success: function(data) { secrets.push(data); },
				  async: false
				});
			});
		}
		$.post('/discussion/'+DISCUSSION_ID+'/comment/', {text: this.parentElement.find('textarea.comment').val(), secrets: secrets.join(',')}, function(data) { location.reload(); });
		return false;
	}
};

$(document).ready(function() {
	secretListController.init($('.discussion_reply_form'));
});
