# import necessary libraries
from models import create_house, create_rent
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import pandas, sqlite3, csv
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
from sqlalchemy import Column, Integer, String, Float

# flask setup
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', '') or "sqlite:///db.sqlite"

# Remove tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Establish Connection
engine = create_engine(
'sqlite:///rent_house.sqlite',
connect_args={'check_same_thread': False}
)

conn = engine.connect()

house_df = pandas.read_csv("static/data/house_filtered.csv")
house_df.to_sql("House", conn, if_exists='replace', index=False)

rent_df = pandas.read_csv("static/data/rent_cleaned.csv")
rent_df.to_sql("Rent", conn, if_exists='replace', index=False)

Rent = create_rent(db)
House = create_house(db)

from sqlalchemy.orm import Session
session = Session(bind=engine)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Return template and data
    return render_template("index.html", title="Loan Helper", )
@app.route("/about")
def about():
    # Return template and data
    return render_template("about.html", title="About")

if __name__ == "__main__":
    app.run(debug=True)