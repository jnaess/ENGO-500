// Initialize the map
var this_map = L.map('map').setView([50.64146,-113.64648], 13);

// Add baselayer
L.tileLayer('https://api.mapbox.com/styles/v1/eprosser88/cl19riul2003215pcc5nlw7b9/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiZXByb3NzZXI4OCIsImEiOiJja3p5d3FoNm4wNGo1M2tuZmNnaHphc2cxIn0.gguHDZWaDus2L4AW0h97rA', {
    id: 'satellitestreets',
    tileSize: 512,
    zoomOffset: -1,
    minZoom: 1,
	attribution: '©  <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="https://www.openstreetmap.org/about/">OpenStreeMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a </strong> © <a href="https://www.maxar.com/">Maxar'
}).addTo(this_map);

// Add scale
L.control.scale().addTo(this_map);