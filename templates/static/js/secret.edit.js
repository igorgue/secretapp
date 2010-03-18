/*
Handler for dealing with creating new Secrets

Author: Tim Davey
Site: http://secretcities.com
*/

var render_template = function(template, dictionary){
    /*
    Takes a given template and dictionary of elements
    
    >>> dictionary := {'title': 'Cool Secret', 'pk': 4}
    >>> template := '<span id='__pk__'>__title__</span>'
    "<span id='4'>Cool Secret</span>"
    */
    var html = template;
    for (key in dictionary){
        html = html.replace(new RegExp('__'+key+'__', "g"), dictionary[key]);
    }
    return html;
}

var secretCreateController = function(config) {
    /*
    Controller which builds default object
    Then updates this object with given config.
        -- See object definition comments for required config elements
    */
    object = {
        /*
        Required:
            title_field := jQuery(input) --where the title should be detected from
            location_field := jQuery(input) --where the human readable address should be detected from
            
            google_map := jQuery(div) --where the map is loaded into
            
            existing_list := jQuery(ul) --where the existing secret suggestions should be populated to
            google_list := jQuery(ul) --where the google results should be populated to
            
            *_list_success := jQuery(div) --elm to be shown on success
            *_list_fail := jQuery(div) --elm to be shown on fail
        Optional:
        
        Default:
            DEFINED BELOW
        */
        existing_secret_url : '/secrets/', // url to query for existing secrets
        local_extra : '', // extra search param for google (append) e.g. ' near London'
        
        existingSearch      : {},
        localSearch         : new GlocalSearch(),
        geocoder            : new GClientGeocoder(),
        
        existing_secret_template : '<li class="isecret"><h4><a class="secret_result" id="si___sreff__" href="#">__title__</a></h4>__address__</li>',
        local_secret_template : '<li class="isecret"><h4><a class="google_result" id="gi___gireff__" href="#">__titleNoFormatting__</a></h4>__streetAddress__, __region__</li>',
        
        error_message : 'Sorry! But an error occurred, could you please try again.',

        getExistingSecrets  : function(search){
            /*
            Description:
                makes an ajax request to secretcities.com/secrets/
                to find any existing secrets which match the passed search term
            Takes:
                `search` := str
            Returns:
                json response of possible secrets
                -- see api for details
            */
            var self = this;
            $.ajax({
                url: self.existing_secret_url,
                data : {
                    'title': search
                },
                dataType: 'json',
                success: function(data){
                    self.existingSearch.results = data;
                    self.renderExistingSecrets();
                },
                error: function(){
                    // silent error
                    // alert(self.error_message);
                }
            });
        },
        renderExistingSecrets : function(){
            /*
            Description:
                renders secrets in a list of possible options
                or shows fail element
            Takes:
                nothing
                -- must call getExistingSecrets
                   renders results from existingSearch
                -- must have defined
                   existing_list
                   existing_list_fail
            Returns:
                nothing
            */
            var results = this.existingSearch.results;
            
            if (results.length > 0){
                
                // clears existing examples
                this.existing_list.html('');
                // renders the new examples
                for (var i=0; i < results.length && i < 5; i++){
                    var result= results[i];
                    result.sreff = i; // used when selecting
                    var html = render_template(this.existing_secret_template, result);
                    this.existing_list.append(html); // appends the new ones
                }
                // handles the rest
                this.existing_list_success.show();
                this.existing_list_fail.hide();
            } else {
                
                this.existing_list_success.hide();
                this.existing_list_fail.show();
            }
            
            this.renderResults();
        },
        
        getGoogleLocalSecrets : function(search){
            /*
            Description:
                Searches google localsearch for businesses
                in the area which match the search term
            Takes:
                search term := str --address of business (including name)
            Returns:
                json response of google results
                -- see google api for details
            */
            var self = this;
            this.localSearch.setSearchCompleteCallback(null, function(){self.renderGoogleLocalSecrets();});
            this.localSearch.execute(search);
        },
        
        renderGoogleLocalSecrets : function(){
            /*
            Description:
                Renders the 
            Takes:
                nothing
                -- however does require that getGoogleLocalSecrets has been called
                   will try and render the results from this.localSearch.results
            */
            var results = this.localSearch.results;
            if (results.length > 0){
                
                // clears existing examples
                this.google_list.html('');
                
                // renders the new examples
                for (var i=0; i < results.length && i < 5; i++){
                    var result = results[i];
                    result.gireff = i; // used when selecting
                    var html = render_template(this.local_secret_template, result);
                    this.google_list.append(html); // appends the new ones
                }
                // handles the rest
                this.google_list_success.show();
                this.google_list_fail.hide();
            } else {
                this.google_list_success.hide();
                this.google_list_fail.show();
            }
            
            this.renderResults();
            
        },
        
        renderResults: function(){
            if( this.localSearch.results.length > 0 || this.existingSearch.results.length > 0)
            {
                this.results_success.show();
                this.results_fail.show();
            }
            else
            {
                this.results_success.hide();
                this.results_fail.show();
            }                
        },
        
        getSecrets : function(){
            /*
            Description:
                Tries both google and existing to 
            Takes:
                nothing
                -- uses val of
                   title_field for getExistingSe..
                   title_field + location_field for getGoogleLocalSe..
            */
            var title = this.title_field.val();
            
            this.getExistingSecrets(title);
            this.getGoogleLocalSecrets(title + this.local_extra);
        },
        
        getAddress : function(){
            /*
            Description:
                Calls google to find the latitude and longitude
                based on the location_field val
            Takes:
                location_field must be set and have a value
            Returns:
                sets latitude_field and longitude_field
            */
            var self = this;
            this.geocoder.getLatLng(this.location_field.val() + this.local_extra, function(point){
                self.latitude_field.val(point.lat());
                self.longitude_field.val(point.lng());
                self.setAddress();
            });
        },
        
        setAddress : function(){
            /*
            Description:
                Builds a google map
            Takes:
                google_map and lat, lng need to be set
                latitude_field and longitude_field both needs val
            */    
            var lat = this.latitude_field.val();
            var lng = this.longitude_field.val();
            var latlng = new GLatLng(lat, lng);
            
            // create map if it doesn't exist
            if (typeof this.map !== ''){
                this.google_map.show();
                this.map = new GMap2(this.google_map[0]);
                this.map.addControl(new GLargeMapControl3D());
            }
            // set the center
            this.map.setCenter(latlng, 15);
            this.map.addOverlay(new GMarker(latlng, {draggable: true}));
        },
        
        resetAll : function() {            
            $("#selected_title").val("");
            $("#selected_address").val("");
            $("#id_title").val("");
            $("#id_location").val("");
            $("#id_longitude").val("");
            $("#id_latitude").val("");
            $("#id_google_reff").val("");
            $('#id_secret_id').val("");
            $('#error_message').text("");
            this.google_list.html('');
            this.existing_list.html('');
            this.results_success.hide();
            this.results_fail.hide();
            $("#results_manual").hide();
            $("#google_map").hide();
            this.title_field.removeAttr("disabled");
        }
    }
    
    // updates object with config
    if (typeof config !== 'undefined'){
        for (c in config){
            object[c] = config[c];
        }
    }
    return object;
}


$(document).ready(function(){
    // Defines fields
    var has_started_looking = false;
    var has_finished_looking = false;
   
    var error_message = $("#error_message");
    var existing_secret_id = $('#id_secret_id');
    var title_field = $('#id_title');
    var location_field = $('#id_location');
    var latitude_field = $('#id_latitude');
    var longitude_field = $('#id_longitude');
    var google_reff_field = $('#id_google_reff');
    var results_success = $('#results_success');
    var results_fail = $('#results_fail');
    
    
    // Builds controller
    var control = secretCreateController({
        'title_field': title_field,
        'location_field': location_field,
        'latitude_field': latitude_field,
        'longitude_field': longitude_field,
        
        'google_map': $('#google_map'),
        
        'results_success' : results_success,
        'results_fail' : results_fail,
        
        'existing_list': $('#existing_suggestions'),
        'existing_list_success' : $('#existing_suggestions_success'),
        'existing_list_fail' : $('#existing_suggestions_fail'),
        
        'google_list' : $('#google_suggestions'),
        'google_list_success' : $('#google_suggestions_success'),
        'google_list_fail' : $('#google_suggestions_fail'),
        
        'local_extra': ', ' + CITY + ", " + COUNTRY,
    });
    
    // check to find secrets on title or location blur
    title_field.keyup(function(e){ 
        has_started_looking=true;
        if(e.keyCode != 13)
        {
            if (title_field.val() == "")
                control.resetAll();
            else
                control.getSecrets();     
        }
        else
            return false;
        
    });
    //location_field.keyup(function(){ control.getSecrets() });
    location_field.keyup(function(){ control.getAddress() });
    
    // onload we want to set the address
    if (latitude_field.val() !== '' && longitude_field.val() !== '') {
        control.setAddress();
    }
    
    $(".reset_selected").click( function() { 
        control.resetAll(); 
        swap("#selected_result","#select_result");
        title_field.focus();
        has_finished_looking=false;
        return false;
    });    
    
    function do_manual(){
        $("#results_success").hide();
        $("#error_message").text("");
        swap("#results_fail","#results_manual");
        title_field.attr("disabled","disabled");
        location_field.focus();        
        return false;
    }
    
    function undo_manual(){
        var temp_title = title_field.val();
        control.resetAll();
        title_field.val(temp_title);
        title_field.focus();
        return false;
    }
    
    $('.select_manual').click(function() {
        return do_manual();
    });

    $('.unselect_manual').click(function() {
        return undo_manual();
    });

    $('#close_results').click(function() {
        return do_manual();
    });    
    
    $('#post_response').click(function(){
        error_message.html("");
        if($("#id_response_text").val() == "")
        {
            if(title_field.val() == "")
            {
                error_message.html("Please write a response or mention a secret place");
                return false;
            }
        }
        if(has_started_looking && !has_finished_looking)
        {
            error_message.html("Please finish entering the secret place");
            return false;
        }
        
        return true;
    });
    
    $('#finished_manual').click(function() {
        //set displayed result values
        $("#selected_title").html(title_field.val());
        $("#selected_address").html(location_field.val());
        swap("#select_result","#selected_result");
        has_finished_looking = true;
        return false;
    });    
    
    $('.secret_result').live('click', function() {
        var index = this.id.replace('si_','');
        var result = control.existingSearch.results[index];
        
        // set hidden form values
        existing_secret_id.val(result.pk);
        title_field.val(result.title);
        location_field.val(result.address);
        
        //set displayed result values
        $("#selected_title").html(title_field.val());
        $("#selected_address").html(location_field.val());
        
        //show selected result
        swap("#select_result","#selected_result");
        results_success.hide();
        results_fail.hide();
        has_finished_looking = true;
        
        control.getAddress();
        
        return false;
    });
    
    // when you click on a google result
    $('.google_result').live('click', function(){
        /*
        Description:
            Renders <a class='google_result' id='gi_4'>Use</a>
            When Use is clicked, takes the fourth found result
                found in control.localSearch.results
                applies the values in that data to the correct fields
        */
        var index = this.id.replace('gi_','');
        var result = control.localSearch.results[index];
        var full_location = result.streetAddress;
        if (result.region != "")
            full_location = full_location + ", " + result.region;
       
        // set hidden form values
        title_field.val(result.titleNoFormatting);
        location_field.val(full_location);
        latitude_field.val(result.lat);
        longitude_field.val(result.lng);
        google_reff_field.val(result.url);
        
        //set displayed result values
        $("#selected_title").html(title_field.val());
        $("#selected_address").html(location_field.val());
        
        //show selected result
        swap("#select_result","#selected_result");        
        results_success.hide();
        results_fail.hide();
        has_finished_looking = true;
        
        // reset the map
        control.getAddress();
        return false;
    });
});















