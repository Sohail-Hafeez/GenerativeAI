let map;
let directionsService;
let directionsRenderer;
let routeInfoWindow;

// Predefined MCS locations with coordinates (for routing)
const locations = {
    "Main Gate": { lat: 33.576915, lng: 73.062118 },
    "EE Lawn": { lat: 33.578616, lng: 73.062006 },
    "CS Block": { lat: 33.6432, lng: 72.9925 },
    "Library": { lat: 33.6425, lng: 72.9929 },
    "Hostel": { lat: 33.6439, lng: 72.9931 }
};

// Custom labels for areas
const customLabels = {
    "Main Gate": { lat: 33.576915, lng: 73.062118 },
    "EE Lawn": { lat: 33.578616, lng: 73.062006 },
    "CS Block": { lat: 33.6432, lng: 72.9925 },
    "Library": { lat: 33.6425, lng: 72.9929 },
    "Hostel": { lat: 33.6439, lng: 72.9931 }
};

// Function to create custom HTML labels on the map
function createCustomLabel(map, position, text) {
    const overlay = new google.maps.OverlayView();
    overlay.onAdd = function() {
        const div = document.createElement('div');
        div.style.position = 'absolute';
        div.style.color = 'pink';
        div.style.fontWeight = 'bold';
        div.style.fontSize = '14px';
        div.style.textShadow = '1px 1px 2px black';
        div.innerText = text;
        this.div = div;

        const panes = this.getPanes();
        panes.overlayLayer.appendChild(div);
    };

    overlay.draw = function() {
        const projection = this.getProjection();
        const point = projection.fromLatLngToDivPixel(position);
        this.div.style.left = point.x + 'px';
        this.div.style.top = point.y + 'px';
    };

    overlay.onRemove = function() {
        this.div.parentNode.removeChild(this.div);
    };

    overlay.setMap(map);
}

function initMap() {
    const mcsCenter = { lat: 33.6435, lng: 72.9927 };

    map = new google.maps.Map(document.getElementById("map"), {
        center: mcsCenter,
        zoom: 17,
        mapTypeId: 'satellite', // Satellite view
        restriction: {
            latLngBounds: {
                north: 33.582294,
                south: 33.575576,
                east: 73.066467,
                west: 73.056795
            },
            strictBounds: true,
        },
        streetViewControl: true,
        fullscreenControl: true,
        styles: [
            { featureType: "all", elementType: "labels", stylers: [{ visibility: "off" }] },
            { featureType: "poi", stylers: [{ visibility: "off" }] }
        ]
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({ map: map });

    // Add custom labels
    for (let label in customLabels) {
        createCustomLabel(map, new google.maps.LatLng(customLabels[label].lat, customLabels[label].lng), label);
    }

    // Populate dropdowns
    const fromSelect = document.getElementById("from");
    const toSelect = document.getElementById("to");
    for (let loc in locations) {
        const option1 = document.createElement("option");
        option1.value = loc;
        option1.text = loc;
        fromSelect.add(option1);

        const option2 = document.createElement("option");
        option2.value = loc;
        option2.text = loc;
        toSelect.add(option2);
    }

    // Add event listener for route calculation
    document.getElementById("findRoute").addEventListener("click", () => {
        const from = fromSelect.value;
        const to = toSelect.value;
        if (from === to) {
            alert("Please select different locations!");
            return;
        }
        calculateRoute(from, to);
    });
}

function calculateRoute(from, to) {
    directionsService.route(
        {
            origin: locations[from],
            destination: locations[to],
            travelMode: 'WALKING'
        },
        (response, status) => {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);

                const route = response.routes[0];
                const leg = route.legs[0];

                const distanceText = leg.distance.text;
                const durationText = leg.duration.text;

                // Place InfoWindow at midpoint of route
                const path = route.overview_path;
                const midIndex = Math.floor(path.length / 2);
                const midPoint = path[midIndex];

                if (routeInfoWindow) {
                    routeInfoWindow.close();
                }

                routeInfoWindow = new google.maps.InfoWindow({
                    content: `<strong>Distance:</strong> ${distanceText} <br> <strong>Duration:</strong> ${durationText}`,
                    position: midPoint
                });

                routeInfoWindow.open(map);
            } else {
                alert('Directions request failed due to ' + status);
            }
        }
    );
}
