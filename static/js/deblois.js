function GetCityName() {
  alert(document.getElementById('citySearchBox').value);
  document.getElementById('citySearchBox').value = "";
}

d3.json('/api/house_data/bubblechart', function (error, responseData) {
  if (error) return console.warn(error);

  var red = 'rgb(255, 48, 37)';
  var green = 'rgb(42, 233, 69)';
  var cityX = Array.from({ length: 250 }, (x, i) => i + 1); //number of cities in the house data set (250 cities will be final number)
  var hoverCityText = responseData[0].City.map(i => 'City: ' + i);
  var hoverPriceText = responseData[0].Price.map(i => '<br>Avg House Price 2021: $' + i.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
  var hoverAmountChangeText = responseData[0].MarkerSize.map(i => '<br>Amount Change: $' + (i*1000).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,'));
  var finalHoverText = [];

  for (var i = 0; i < hoverCityText.length; i++) {
    finalHoverText.push(hoverCityText[i] + hoverPriceText[i] + hoverAmountChangeText[i]);
}

  var trace1 = {
    x: cityX,
    y: responseData[0].Price, //house sell price
    text: finalHoverText,
    mode: 'markers',
    marker: {
      size: responseData[0].MarkerSize, //relative price change for 2014 vs 2020
      color: green,
      opacity: 0.3
    }
  };

  var data = [trace1];

  var layout = {
    title: 'House Price 2014 vs. 2021',
    showlegend: false,
    height: 800,
    width: 800
  };

  Plotly.newPlot("plot-garrett", data, layout);
});