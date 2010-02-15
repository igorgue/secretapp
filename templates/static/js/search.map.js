/* 
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

var cfg ={
    //info about config here?
    //@todo change to correct ajax page
    ajaxUrl : "/secrets/", //location of the ajaxPage

    //@todo change here
    domMapId : "map", //for the big map thing


    //miniMapId : "map_canvas", //for the mini map when adding a secret
    //moreInfo : "map_search_results_list", //the div we wil be displaying the list location search results or
                                            // extra results from the db when we search for the secrets
    //lookupAddressTimeout : 1000,
    city : "london"
};

var gmapFn ={
    // @description :
    // @author : Jlee
    defaultIcon : "http://gmaps-samples.googlecode.com/svn/trunk/markers/blue/blank.png",
    mapObj : null, //the actual goog map obj
    mapDom : null,
    lastRefLatLng : 
        {'lat': 0,
         'lng': 0
        }, //the lat lng of the last map refresh
    //localSearch : new GlocalSearch(),
    //localSearch : new google.search.LocalSearch(),

    init : function(domId){
        // set the domid we will have the map in
        if(typeof(domId) == 'undefined'){
            //assume main id
            domId = cfg.domMapId;
        };
        
        if (GBrowserIsCompatible()) {
            this.mapDom = document.getElementById(domId);
            this.mapObj = new GMap2(this.mapDom);
            this.mapObj.setCenter(new GLatLng(51.512880,-0.134334),16);
            largeContol = new GLargeMapControl();
            this.mapObj.addControl(largeContol);
            this.mapObj.disableScrollWheelZoom();

                //set slider min + max zoom levels
            var mapTypes = this.mapObj.getMapTypes();
            for(var i=0; i<mapTypes.length; i++){
                mapTypes[i].getMinimumResolution=function(){return 12;}
                mapTypes[i].getMaximumResolution=function() {return 18;}
            };

            
            GEvent.addListener(this.mapObj,'zoomend',function(){
                gmapFn.addSecretsToMap();
            });
            
        };

    },

    addMarker : function(pntLat, pntLong, markerInfo, markerIcon){
        //@param: string markerIcon - assume may have multiple types of icons for markers on map

            //create the point obj for map
        var point = new GLatLng(pntLat, pntLong);
        if(!markerIcon){
            //assume using default
            markerIcon = this.defaultIcon;
        }

            //prep an icon obj
        var mapIcon = new GIcon(G_DEFAULT_ICON);
        markerOptions = { icon:mapIcon };

            //create the marker
        var marker = new GMarker(point,markerOptions);

        //@todo : how to best to make this generic for all types of markers?
        GEvent.addListener(marker, "mouseup", function() {
            //@todo use alternatuve plugin to googles info panel
                marker.openInfoWindowHtml(markerInfo);
          });


        gmapFn.mapObj.addOverlay (marker);
    },

    showSecretsOnMap : function(mapData){
        //adds all the secrets on the map
        var infoTpl = "<b>xyzMrkTitle</b><p>xyzAdd1";
        infoTpl +="<a href='#' onClick='Alert(\"go to id xyzPk\")'><br>More info</a></p>";//template for floating html
        var mrkTmp = "";
        var i = 0;

        for (i in mapData){
            mrkTmp ='';
            mrkTmp = infoTpl.replace("xyzMrkTitle", mapData[i].title);
            mrkTmp = mrkTmp.replace("xyzMrkInfo",  mapData[i].Description);
            mrkTmp = mrkTmp.replace("xyzAdd1",  mapData[i].address);

            gmapFn.addMarker(mapData[i].lat, mapData[i].long, mrkTmp);
        }
    },

    mapSearch : function(srchPlace,prmpt){
        //Updates the map based on search, geocodes the srchPlace
        //@param: srchPlace search term entered
        //@param: bool prmpt = indicates whether to show cant find addr
        if(typeof(prmpt)=="undefined"){
            prmpt = true;
        }
        this.mapObj.clearOverlays();

        var geocode = new GClientGeocoder();
	geocode.setBaseCountryCode('UK');

        geocode.getLatLng(
            srchPlace + ", uk",
            function(point){
                if (!point) {
                    if(prmpt){
                        alert("Sorry, I couldn't find " + address + ". Do you want to try again?");
                    }
                    return false;
                }
                else{
                    //whoot found it, not show txfhe map
                    gmapFn.mapObj.setCenter(point);
                    return true;
                }
            }
        );
    },
    addSecretsToMap : function(){
        //main function to initiate the adding of holye
        bounds = gmapFn.mapObj.getBounds();
        var swBnd = bounds.getSouthWest();
        var neBnd = bounds.getNorthEast();

        var north = neBnd.lat();
        var east = neBnd.lng();
        var south = swBnd.lat();
        var west = swBnd.lng();
        fetch.getSecretsMap(north, east, south, west,0);
            //update the point of the last refresh
        var ct = mapFn.mainmap.GetCenter()
        mapFn.lastRefLatLng.lat = ct.Latitude;
        mapFn.lastRefLatLng.lng = ct.Longitude;
        //gmapFn.showSecretsOnMap(dat);
    },

    addSpotsInArea : function(searchTerm, address) {
        // does a local search and centers the map based on the location
        //@param searchTerm = the secret being searched for eg pizza hut

        if (typeof(address) == 'undefined') {
            address = getAddress();
        }
        if (!jQuery.trim(address)) {
            return;
        }
        // first we try looking up using the google local ajax search API, which works better for postcodes

            //the search term we will be sending to google local search
        var srchLocal = searchTerm + ' near ' + address + ' , ' + cfg.city;
        // @todo - doh no results being returned when we search!

        srchLocal = "bakery near se14";
        this.localSearch.execute(srchLocal);iv
        this.localSearch.setSearchCompleteCallback(null,
            function() {
                //* @todo - chk ??
                //clearTimeout(lookupAddressTimeout);

                //if we got a geocode to center the map then move to that location
                

                if (gmapFn.localSearch.results[0]) {
                    html = '';
                    resultCount = gmapFn.localSearch.results.length;
                    for (i = 0; i < resultCount; i++) {
                        r = gmapFn.localSearch.results[i];
                        html += '<li><a href="#" onclick="selectMapResult(' + r.lat + ',' + r.lng + ',\'' + r.titleNoFormatting.replace('\'', '\\\'') + '\',\'' + r.streetAddress.replace('\'', '\\\'') + '\'); return false;">' + r.title;
                        if (r.streetAddress != r.title) { html += ', ' + r.streetAddress; }
                            html += '</a></li>';
                    }
                    $('#' + cfg.locList).append(html);
                }
 /*
                else{
                    // if local search fails, we try the geocode address search
                if(geocoder) {
                    geocoder.getLatLng(
                        address + ', London',
                        function(point) {
                            // we detect center of london as "no result"
                            if (!point || ((point.lat() == 51.5001524) && (point.lng() == -0.1262362))) {
                                noMapResults();
                            }
                            else{
                                selectMapResult(point.lat(), point.lng());
                            }
                        });
                    }
                }
*/
            });//first closure

        },

    addGoogLocal : function(){
        //adds local info results
        $('#'+cfg.moreInfo).append('<br>Info from google ssearch');
    }
}



var fetch = {
  // @description : this objecy is the data access model obj thingy.
  //    all data returned from functions should be JSON
  // @author : Jlee

    getSecretsMap : function(north, east, south, west){

        var dat = null;
        /*
        var latLng = {
            "swLat" : swLat,
            "swLng" : swLng,
            "neLat" : neLat,
            "neLng" : neLng
            };
        */
        var latLng = {
            "west" : west,
            "south" : south,
            "north" : north,
            "east" : east
            };
        $.ajax({
            url: cfg.ajaxUrl,
            data : latLng,
            cache: false, 
            success: function(data) {
                var info = eval(data)
                gmapFn.showSecretsOnMap(info);
                //alert('Load was performed.');
            }
        });
        
        var mapData = [
            {
                "PK_Secret" : 1,
                "Title" : "Secret 1 - a nice restaurant",
                "Description"   : "This is a nice restaurant",
                "Address 1" : "1 Shaftsbury Avenue",
                "Address 2" : "London",
                "Post Code" : "",
                "Lat" : 51.51167048188837,
                "Long" : -0.13294100761413574,
                "ImgThumb" : "http://farm4.static.flickr.com/3179/2325517070_1a58e07491_t.jpg",
                "ImgLarge" : "http://farm4.static.flickr.com/3179/2325517070_1a58e07491_b.jpg",
                "markerIcon" : ""
            },
            {
                "PK_Secret" : 2,
                "Title" : "Glasshouse Stores - Sam smith pub",
                "Description"   : "A nice sam smith pub in london",
                "Address 1" : "55 Brewer Street",
                "Address 2" : "London",
                "Post Code" : "W1F 9UN",
                "Lat" : 51.51167382046179,
                "Long" : -0.13539791107177734,
                "ImgThumb" : "http://farm4.static.flickr.com/3213/2711833744_74ebc2dff5_t.jpg",
                "ImgLarge" : "http://farm4.static.flickr.com/3213/2711833744_74ebc2dff5_b.jpg",
                "markerIcon" : ""
            }];

        // fake data
        //return mapData;

        return dat;
    },

    getFindSecretNames : function(srch){
        //searches the db for secrets with same/similar names
/*
        $.ajax({
            url: cfg.ajaxUrl,
            success: function(data) {
                alert('searching for stuff');
            },
            data : srch
        });
*/
        var s = [
            {
                "Name" : "Bakery Joe"
            },
            {
                "Name" : "Another bakery"
            },
            {
                "Name" : "ttttt bakery"
            }
        ];
        return s;


    }
}

var addSct = {
  // @description : functions for adding a secret form
  // @author : Jlee

    chkExist : function(secretTxt){
        //checks with backend whether secret exists or not
        var sName = $('#secretName').val();
        var dat = fetch.getFindSecretNames(sName)

            //chk if data in db
        if(dat.length>0){
            //add it to the
            $('#' + cfg.moreInfo).html('Hey Mr Database just noticed that looks suspeciously like... <p>');

            var tpl ='<a href="xyzLink">xyzName</a><br>';
            var tmp = null;
            var t1 = '';
            $.each(dat,function(index,value){
                tl = value.Name;
                tmp = tpl.replace('xyzName',tl);
                $('#' + cfg.moreInfo).append(tmp);
            });
        }

        

    }
}


$(document).ready(function() {
    /***
     * Bind behaviour
     */
    // area search
    $('#areaFrm').submit(function(){
        return false;
    });
    $('#searchFor').click(function(){
        $(this).val('');
    });
    $('#areaSrchBtn').click(function(){
        gmapFn.mapSearch($('#searchFor').val());
        gmapFn.addSecretsToMap();
    });

    //"secrets" search
    $('#wordSecretSrch').click(function(){
        $(this).val('');
    });
    $('#secretSrchBtn').click(function(){
        alert('Gonna search for secrets')
    });

    /**adding a secret form **/
    $('#secretName').keyup(function(){
        //chk the database where when we type more then 3 chars
            if ($(this).val() == "eg Bob bakerys"){
                $(this).val('')
            }
            var t = $(this).val();
            t = t.replace(" ","");
            if(t.length > 3 && t!== "eg Bob bakerys"){
                addSct.chkExist();
            };
            if(t.length > 6){
                $('#secretAddInfo').html('checking google now');
            }
         })

    //where text box/location search
    $('#whereInp').keyup(function(){
            if($(this).val() == 'e.g Soho or w10 5dt'){
                $(this).val('');
            }
            var t = $(this).val();
            t = t.replace(" ","");

            if(t.length > 1){
                //do the location search-
                gmapFn.init("miniMap");
                gmapFn.mapSearch($(this).val(),false);
                gmapFn.addGoogLocal();
                gmapFn.addSpotsInArea($('#secretName').val(), $(this).val());
            };
    })

    $('#frmShare').submit(function(){
        return false;
    });

    /** adding a new secret?
     * http://beta.secretlondon.us/secret/new/ **/


    /***
     * other stuff
     */

    // chk if we have a main map
    if($('#'+cfg.domMapId).length > 0){
        gmapFn.init();
        // add markers to the map
            //get data
        var mapData = fetch.getSecretsMap(0, 0, 0);
        gmapFn.showSecretsOnMap(mapData);
    }

})

