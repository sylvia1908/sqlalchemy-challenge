import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitations<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/ends_date"
    )


@app.route("/api/v1.0/precipitations")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    last_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).scalar(), '%Y-%m-%d') \
                                        - dt.timedelta(days=365)
    results = session.query(Measurement) \
        .filter(Measurement.date >last_date ) \
        .all()

    session.close()

    # Convert list of tuples into normal list
    data= []

    for obj in results:
        row = {}
        row['date']= obj.date
        row['prcp']= obj.prcp
        data.append(row)

    return jsonify(data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)


    # Query all Station
    results = session.query(Station.name).all()

    session.close()

    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))

    return jsonify(all_names)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

 
    # Convert the query results to a Dictionary using date as the key and prcp as the value.
    last_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).scalar(), '%Y-%m-%d') \
                                        - dt.timedelta(days=365)
    results = session.query(Measurement) \
        .filter(Measurement.date >last_date ) \
        .all()

    session.close()

    # Convert list of tuples into normal list
    data= []

    for obj in results:
        row = {}
        row['date']= obj.date
        row['tobs']= obj.prcp
        data.append(row)

    return jsonify(data)

@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start, end):

    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    return jsonify(result)

@app.route("/api/v1.0/<start>")
def calc(start):

    session = Session(engine)
    result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
