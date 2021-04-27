function calculate() {
  //Look up the input and output elements in the document
  var homeprice = document.getElementById("home_price");
  var downpayment = document.getElementById("down_payment");
  var apr = document.getElementById("apr");
  var years = document.getElementById("years");
  var payment = document.getElementById("payment");
  var total = document.getElementById("total");
  var totalinterest = document.getElementById("totalinterest");
  var printerest = document.getElementById("printerest");
  var taxesfee = document.getElementById("taxesfee");
  var homeinsurance = document.getElementById("homeinsurance");

  // Get the user's input from the input elements.
  // Convert interest from a percentage to a decimal, and convert from
  // an annual rate to a monthly rate. Convert payment period in years
  // to the number of monthly payments.
  var principal = parseFloat(homeprice.value - downpayment.value);
  var interest = parseFloat(apr.value) / 100 / 12;
  var payments = parseFloat(years.value) * 12;

  // compute the monthly payment figure
  var x = Math.pow(1 + interest, payments); //Math.pow computes powers
  var monthly = (principal * x * interest) / (x - 1);
  var homeinsur = (monthly * 0.105);
  var taxesfees = (monthly * 0.41);

  // If the result is a finite number, the user's input was good and
  // we have meaningful results to display
  if (isFinite(monthly)) {
    // Fill in the output fields, rounding to 2 decimal places
    printerest.innerHTML = (monthly).toFixed(2);
    taxesfee.innerHTML = (taxesfees).toFixed(2);
    homeinsurance.innerHTML = (homeinsur).toFixed(2);
    payment.innerHTML = (monthly + homeinsur + taxesfees).toFixed(2);
    loanamount.innerHTML = principal;
    total.innerHTML = (monthly * payments).toFixed(2);
    totalinterest.innerHTML = ((monthly * payments) - principal).toFixed(2);

    // Finally, chart loan balance, and interest and equity payments
    chart(principal, interest, monthly, payments);
  }
  else {
    // Result was Not-a-Number or infinite, which means the input was
    // incomplete or invalid. Clear any previously displayed output.
    loanamount.innerHTML = "";
    payment.innerHTML = ""; // Erase the content of these elements
    total.innerHTML = "";
    totalinterest.innerHTML = "";
    homeinsurance.innerHTML = "";
    taxesfee.innerHTML = "";
    printerest.innerHTML = "";

    chart(); // With no arguments, clears the chart
  }
}
// Chart monthly loan balance, interest and equity in an HTML <canvas> element.
// If called with no arguments then just erase any previously drawn chart.
function chart(principal, interest, monthly, payments) {
  var trace1 = {
    x: [1, 2, 3, 4],
    y: [0, 2, 3, 5],
    fill: 'tozeroy',
    type: 'scatter'
  };
  
  var trace2 = {
    x: [1, 2, 3, 4],
    y: [3, 5, 1, 7],
    fill: 'tonexty',
    type: 'scatter'
  };
  
  var data = [trace1, trace2];
  
  Plotly.newPlot('plotly', data);
}