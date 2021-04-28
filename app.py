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
pipeline = load('logistic.joblib')

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
        gender = int(request.form['gender'])
        married = int(request.form['married'])
        dependents = int(request.form['dependents'])
        if dependents == 0:
            dependents_zero = 1
            dependents_one = 0
            dependents_two = 0
            dependents_three = 0 
        elif dependents == 1:
            dependents_zero = 0
            dependents_one = 1
            dependents_two = 0
            dependents_three = 0 
        elif dependents == 2:
            dependents_zero = 0
            dependents_one = 0
            dependents_two = 1
            dependents_three = 0 
        else:
            dependents_zero = 0
            dependents_one = 0
            dependents_two = 0
            dependents_three = 1 
        education = int(request.form['education'])
        self_employed = int(request.form['self_employed'])
        property_area = int(request.form['property_area'])
        if property_area == 0:
            rural = 1
            semiurban = 0
            urban = 0 
        elif property_area == 1:
            rural = 0
            semiurban = 1
            urban = 0
        else:
            rural = 0
            semiurban = 0
            urban = 1
 

        #put the variables into a pandas dataframe
        df = pd.DataFrame({
            'ApplicantIncome': [applicant_income],
            'CoapplicantIncome': [coapplicant_income],
            'LoanAmount': [loan_amount],
            'Loan_Amount_Term': [loan_amount_term],
            'Credit_History': [credit_history],
            'Gender_Male': [gender],
            'Married_Yes': [married],
            'Dependents_0': [dependents_zero],
            'Dependents_1': [dependents_one],
            'Dependents_2': [dependents_two],
            'Dependents_3+': [dependents_three],
            'Education_Graduate': [education],
            'Self_Employed_Yes': [self_employed],
            'Property_Area_Rural': [rural],
            'Property_Area_Semiurban': [semiurban],
            'Property_Area_Urban': [urban]
        })

        pred_cols = list(df.columns.values)
        prediction = pipeline.predict(df[pred_cols])[0]
        if prediction == 0:
            decision = 'Denied'
        if prediction == 1:
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