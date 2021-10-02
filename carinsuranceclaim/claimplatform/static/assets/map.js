
function initMap() {

  // The location of Uluru
  const uluru = { lat: 6.0866266, lng: 100.306586 };
  // The map, centered at Uluru
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom:16,
    center: uluru,
  });
  // The marker, positioned at Uluru
  const marker = new google.maps.Marker({
    position: uluru,
    map: map,
    disableDefaultUI: false, // Disables the controls like zoom control on the map if set to true
     scrollWheel: true, // If set to false disables the scrolling on the map.
    draggable: true,
  }
  );
     // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });

  let markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];
    
    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        })
      );
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
   
  });



  var addressEl = document.querySelector( '#pac-input' )
  google.maps.event.addListener( marker, "dragend", function ( event ) {
    var lat, long, address, resultArray, citi;

    console.log( 'i am dragged' );
    lat = marker.getPosition().lat();
    long = marker.getPosition().lng();

    var geocoder = new google.maps.Geocoder();
    geocoder.geocode( { latLng: marker.getPosition() }, function ( result, status ) {
        if ( 'OK' === status ) {  // This line can also be written like if ( status == google.maps.GeocoderStatus.OK ) {
            address = result[0].formatted_address;
            resultArray =  result[0].address_components;

            // Get the city and set the city input value to the one selected
            for( var i = 0; i < resultArray.length; i++ ) {
                if ( resultArray[ i ].types[0] && 'administrative_area_level_2' === resultArray[ i ].types[0] ) {
                    citi = resultArray[ i ].long_name;
                    console.log( citi );
                    city.value = citi;
                }
            }
            addressEl.value = address;
            latEl.value = lat;
            longEl.value = long;

        } else {
            console.log( 'Geocode was not successful for the following reason: ' + status );
        }

        // Closes the previous info window if it already exists
        if ( infoWindow ) {
            infoWindow.close();
        }

        /**
         * Creates the info Window at the top of the marker
         */
        infoWindow = new google.maps.InfoWindow({
            content: address
        });

        infoWindow.open( map, marker );
    } );
});

}
