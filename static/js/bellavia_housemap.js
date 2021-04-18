// Creating map object
var myMap = L.map("map", {
  center: [37.09024, -95.712891],
  zoom: 5
});

// Adding tile layer to the map
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// Store API query variables
const house_url = "/api/house_data/1/2020/"

d3.json(house_url, function (response) {
  console.log(response);
  var heatArray = [];
  for (var i = 0; i < response[0].Year.length; i++) {

    var place = [response[0].City[i], response[0].Lat[i], response[0].Lng[i], response[0].Price[i], response[0].State[i]];
    var m = Math.round(place[3] / 100);
    for (var j = 1; j < m; j++) {

      heatArray.push([place[1], place[2]]);
    }
    L.marker([place[1], place[2]])
        .bindPopup(place[0] + ", " + place[4] + "<br>Typical Home Value: $" + place[3]).addTo(myMap);
    
  }
  console.log(heatArray);
  var heat = L.heatLayer(heatArray, {
    radius: 25,
    blur: 35
  }).addTo(myMap);

});