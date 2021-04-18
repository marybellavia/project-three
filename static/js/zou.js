// Store API query variables
const rentalapi_url = "https://raw.githubusercontent.com/marybellavia/project-two/main/static/data/rent_cleaned.csv/rent_data"

Plotly.d3.json(rentalapi__url, function(rows){

      function unpack(rows, key) {
          return rows.map(function(row) { return row[key]; });
      }

  var allStateNames = unpack(rows,'State'),
      allYear = unpack(rows,'Year'),
      allPrice = unpack(rows,'Price'),
      listofStates = [],
      currentState,
      currentPrice = [],
      currentYear = [];
      listofStates.split(',');
    for (var i = 0; i < allStateNames.length; i++ ){
      if (listofStates.indexOf(allStateNames[i]) === -1 ){
          listofStates.push(allStateNames[i]);
      }
    }
    
  function getStateData(chosenState) {
    currentPrice = [];
    currentYear = [];
    for (var i = 0 ; i < allStateNames.length ; i++){
      if ( allStateNames[i] === chosenState) {
        currentPrice.push(allPrice[i]);
        currentYear.push(allYear[i]);
      } 
    }
  };

// Default State Data
setBubblePlot('New York');
  
function setBubblePlot(chosenState) {
    getStateData(chosenState);  

    var trace1 = {
      x: currentYear,
      y: currentPrice,
      mode: 'lines+markers',
      marker: {
        size: 12, 
        opacity: 0.5
      }
    };

    var data = [trace1];

    var layout = {
      width:800,
      hight:800,
      title: 'Price for rental by State<br>'+ chosenState + ' Price'
    };

    Plotly.newPlot("plot-irene", data, layout,{showSendToCloud: true});
};
  
var innerContainer = document.querySelector('[data-num="0"'),
    plotEl = innerContainer.querySelector('.plot'),
    stateSelector = innerContainer.querySelector('.statedata');

function assignOptions(textArray, selector) {
  for (var i = 0; i < textArray.length;  i++) {
      var currentOption = document.createElement('option');
      currentOption.text = textArray[i];
      selector.appendChild(currentOption);
  }
}

assignOptions(listofStates, stateSelector);

function updateState(){
    setBubblePlot(stateSelector.value);
}
  
stateSelector.addEventListener('change', updateState, false);
});

