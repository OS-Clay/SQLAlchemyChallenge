from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect




engine = create_engine("sqlite:////tmp/hawaii.sqlite")
#again, i had to put the sqlite file in tmp, be sure to change this when run

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return """
    Welcome to Clay's Hawaii Climate API!
    Available endpoints: <br>
    /api/v1.0/precipitation <br>
    /api/v1.0/stations <br>
    /api/v1.0/tobs <br>
    /api/v1.0/&lt;start&gt; where start is a date in YYYY-MM-DD format <br>
    /api/v1.0/&lt;start&gt;/&lt;end&gt; where start and end are dates in YYYY-MM-DD format
    """

@app.route("/api/v1.0/precipitation")
def precip():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()

    results_dict = []
    for row in results:
        date_dict = {}
        date_dict[row.date] = row.prcp
        results_dict.append(date_dict)

    return jsonify(results_dict)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    results_list = list(results)

    return jsonify(results_list)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= "2016-08-23").all()

    results_list = list(results)

    return jsonify(results_list)


def desc_temps(date1):

    return session.query(func.MAX(Measurement.tobs), func.MIN(Measurement.tobs), func.AVG(Measurement.tobs)).\
    filter(Measurement.date >= date1).all()

@app.route("/api/v1.0/<start>")
def start_date(start):

    end_date = session.query(func.max(Measurement.date)).all()[0][0]
    temps = desc_temps(start)
    temps_list = list(temps)
    return jsonify(temps_list)

def desc_temps_2(date1, date2):

    return session.query(func.MAX(Measurement.tobs), func.MIN(Measurement.tobs), func.AVG(Measurement.tobs)).\
    filter(Measurement.date >= date1).filter(Measurement.date <= date2).all()


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    temps = desc_temps_2(start, end)
    temps_list = list(temps)
    return jsonify(temps_list)

if __name__ == '__main__':
    app.run(debug=True)
