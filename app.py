# Import dependencies
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Import Flask
from flask import Flask, redirect, jsonify


# Database Setup
# Create connection to the sqllite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create session (link) from Python to the DB
session = Session(engine)
# Flask Setup
app = Flask(__name__)
# Flask Routes
#List all available api routes.
@app.route("/")
def welcome():
     return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#Convert query results to a dictionary using date as the key and tobs as the value
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query Measurement
    results = (session.query(Measurement.date, Measurement.tobs).order_by(Measurement.date))
    
    # Create a dictionary
    precipitation_date_tobs = []
    for each_row in results:
        dt_dict = {}
        dt_dict["date"] = each_row.date
        dt_dict["tobs"] = each_row.tobs
        precipitation_date_tobs.append(dt_dict)

    return jsonify(precipitation_date_tobs)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/station")
def stations():
    results = session.query(Station.name).all()
    # Convert list of tuples into normal list
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

if __name__ == "__main__":
    app.run(debug=True) 
