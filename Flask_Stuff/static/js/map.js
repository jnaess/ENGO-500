// Initialize the map
var this_map = L.map('map').setView([51.0447, -114.0719], 11);

// Add baselayer
L.tileLayer('https://api.maptiler.com/maps/streets/{z}/{x}/{y}.png?key=cEgaV9M2KZkGEYF5k2vO',{
       tileSize: 512,
       zoomOffset: -1,
       minZoom: 1,
       attribution: "\u003ca href=\"https://www.maptiler.com/copyright/\" target=\"_blank\"\u003e\u0026copy; MapTiler\u003c/a\u003e \u003ca href=\"https://www.openstreetmap.org/copyright\" target=\"_blank\"\u003e\u0026copy; OpenStreetMap contributors\u003c/a\u003e",
       crossOrigin: true
     }).addTo(this_map);

// Add scale
L.control.scale().addTo(this_map);