import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# db
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

# Flask
app = Flask(__name__)

@app.route("/")
def welcome():
    return "Welcome to the Climate App! Below are all available api routes: </br>" + \
            f"/api/v1.0/precipitation</br>" + \
            f"/api/v1.0/stations</br>" + \
            f"/api/v1.0/tobs</br>" + \
            f"/api/v1.0//api/v1.0/<start>` and `/api/v1.0/<start>/<end>`"

@app.route("/api/v1.0/precipitation/")
def precipitation():
    precip = session.query(measurement.date, measurement.tobs).all()
    precip_dict = dict(precip)
    return jsonify(precip_dict)

@app.route("/api/v1.0/station/")
def stations():
    stations = session.query(station.name).all()
    stations = [station[0] for station in stations]
    return jsonify(stations)

@app.route("/api/v1.0/tobs/")
def tobs():
    tobs = session.query(measurement.tobs).all()
    tobs = [tobs[0] for tobs in tobs]
    return jsonify(tobs)

@app.route("/api/v1.0/<start>/")
# when given only start date, calculate date to present
def start():
    start = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        group_by(measurement.date).all()

    start_dict = {}
    start_dict["TMIN"] = start[0][1]
    start_dict["TAVG"] = start[0][2]
    start_dict["TMAX"] = start[0][3]
        
    return jsonify(start_dict)

@app.route("/api/v1.0/<start>/<end>")
# when given start & end, calculate between these two dates
def start_end(start, end):
    start_end = session.query(measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date <= end).\
        filter(measurement.date >= start).all()
  
    startend_dict = {}
    startend_dict["TMIN"] = start_end[0][1]
    startend_dict["TAVG"] = start_end[0][2]
    startend_dict["TMAX"] = start_end[0][3]
           
    return jsonify(startend_dict)

if __name__ == '__main__':
    app.run(debug=True)
