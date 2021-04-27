# import necessary libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect,
    session, 
    flash)
import pandas as pd
import numpy as np
from joblib import load

# flask setup
app = Flask(__name__)
pipeline = load('loan_predictor.joblib')

#form validation function for text fields
def ReplaceChars(text):
    if text is "" or text is None:
        text = 0 #if text box is empty default the value to 0
    else:
        chars = ",$" #removing common monetary and numeric formatting
        for c in chars:
            text = text.replace(c, '')
        if '.' in text:
            text = int(float(text)) #typecasting to float then to int to drop the decimal places
    return text

# Route to render index.html template
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html", title="Loan Helper")
@app.route("/about")
def about():
    # Return template and data
    return render_template("about.html", title="About")
@app.route("/prediction", methods=['POST', 'GET'])
def prediction():
    # Return template and data

    #take user input from Form as a Post request and typecast it to the proper data structure
    if request.method == 'POST':
        gender = int(request.form['gender'])
        married = int(request.form['married'])
        dependents = int(request.form['dependents'])
        education = int(request.form['education'])
        self_employed = int(request.form['self_employed'])

        try:
            applicant_income = int(ReplaceChars(str(request.form['applicant_income'])))
        except ValueError:
            return render_template('prediction.html', title="Loan Prediction", decision="Invalid input on Current Yearly Income field.")
        try:
            coapplicant_income = int(ReplaceChars(str(request.form['coapplicant_income'])))
        except ValueError:
            return render_template('prediction.html', title="Loan Prediction", decision="Invalid input on Coapplicant Yearly Income field.")
        try:
            loan_amount = int(ReplaceChars(str(request.form['loan_amount'])))
        except ValueError:
            return render_template('prediction.html', title="Loan Prediction", decision="Invalid input on Desired Loan Amount field.")

        loan_amount_term = int(request.form['loan_amount_term'])
        credit_history = int(request.form['credit_history'])
        property_area = int(request.form['property_area'])

        #put the variables into a pandas dataframe
        df = pd.DataFrame({
            'Gender': [gender],
            'Married': [married],
            'Dependents': [dependents],
            'Self_Employed': [self_employed],
            'ApplicantIncome': [applicant_income],
            'CoapplicantIncome': [coapplicant_income],
            'LoanAmount': [loan_amount],
            'Loan_Amount_Term': [loan_amount_term],
            'Credit_History': [credit_history],
            'Property_Area': [property_area]
        })

        pred_cols = list(df.columns.values)
        prediction = pipeline.predict(df[pred_cols])[0]
        if prediction == 'N':
            decision = 'Denied'
        if prediction == 'Y':
            decision = 'Approved'

        return render_template('prediction.html', title="Loan Prediction", decision=decision)

    decision = "Fill out the form on the left."
    return render_template("prediction.html", title="Loan Prediction", decision=decision)
@app.route("/infographics")
def infographics():
    # Return template and data
    return render_template("infographics.html", title="Loan Infographics")
@app.route("/calculator")
def calculator():
    # Return template and data
    return render_template("calculator.html", title="Payment Calculator")



if __name__ == "__main__":
    app.run(debug=True)