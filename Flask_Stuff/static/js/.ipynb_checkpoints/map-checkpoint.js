// Initialize the map
var this_map = L.map('map').setView([51.0447, -114.0719], 11);

// Add baselayer
    L.tileLayer('http://mts3.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',{
        maxZoom:22,
        maxNativeZoom:18
    }).addTo(this_map);

// Add scale
L.control.scale().addTo(this_map);