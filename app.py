import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
engine =  create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)


Measurement = Base.classes.measurement
Station = Base.classes.station


app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    first = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    time_delta = dt.date(2017,8,23) - dt.timedelta(days=366)
    one_year_data = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > time_delta).\
        filter(Measurement.date < dt.date(2017,8,24)).all()
    prcp = []

    for date, percp in one_year_data:
        dic = {}
        dic["date"] = date
        dic["precipitation"] = percp
        prcp.append(dic)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    station = session.query(Measurement.station).\
              group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temp_obsr():
    session = Session(engine)
    first1 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    time_delta1 = dt.date(2017,8,23) - dt.timedelta(days=366)
    one_year_data1 = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.date > time_delta1).\
        filter(Measurement.date < dt.date(2017,8,24)).all()
    tm_obs = []

    for date, tmp_obs in one_year_data1:
        dic_tmp = {}
        dic_tmp["date"] = date
        dic_tmp["Temp_observation"] = tmp_obs
        tm_obs.append(dic_tmp)

    return jsonify(tm_obs)

@app.route("/api/v1.0/<start>")
def temp_for_startday(start):
    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
             filter(Measurement.date >= start).all()
    final_values = []
    for tmin,tavg,tmax in result:
        final_dic = {}
        final_dic["Min Temp"] = tmin
        final_dic["Avg Temp"] = tavg
        final_dic["Max Temp"] = tmax
        final_values.append(final_dic)
    return jsonify(final_values)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start,end):
    session = Session(engine)
    results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
               filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    final_result = []
    for tmin,tavg,tmax in results:
        final_dic1 = {}
        final_dic1["Min Temp"] = tmin
        final_dic1["Avg Temp"] = tavg
        final_dic1["Max Temp"] = tmax
        final_result.append(final_dic1)
    return jsonify(final_result)


if __name__ == '__main__':
    app.run(debug=True)

