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
        applicant_income = int(request.form['applicant_income'])
        coapplicant_income = int(request.form['coapplicant_income'])
        loan_amount = int(request.form['loan_amount'])
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
    #TODO return the result (accepted/denied as a string) from the algo as a string and store the result in a new webpage the user will be redirected to

    decision = "Fill out the form on the left."
    return render_template("prediction.html", title="Loan Prediction", decision=decision)
@app.route("/infographics")
def infographics():
    # Return template and data
    return render_template("infographics.html", title="Loan Infographics")

if __name__ == "__main__":
    app.run(debug=True)