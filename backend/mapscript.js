let map, service, infowindow;

function initMap() {
    // Initialize the map
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 37.7749, lng: -122.4194 }, // Default location (San Francisco)
        zoom: 10,
    });

    // Initialize the search box
    const searchBox = new google.maps.places.SearchBox(document.getElementById("search-box"));

    // When the user selects a location, zoom in on that location
    searchBox.addListener("places_changed", function() {
        const places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers
        const bounds = new google.maps.LatLngBounds();

        places.forEach(function(place) {
            if (!place.geometry || !place.geometry.location) {
                console.log("Returned place contains no geometry");
                return;
            }

            // Zoom in on the selected place
            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });
}

// Load the map when the page loads
window.onload = initMap;
