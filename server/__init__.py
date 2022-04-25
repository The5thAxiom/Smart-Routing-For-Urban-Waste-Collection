from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api
db = SQLAlchemy(app)

from server.models import *
db.create_all()

@app.route('/')
def index_route():
    return render_template('index.html', **{
        "heading": "Smart Routing for Urban Waste Collection",
        "by": "Samridh"
    })

@app.route('/view-db')
def viewDB_route():
    return render_template('viewDb.html', ** {
        "bins": Bin.query.all(),
        "binData": BinData.query.all()
    })

@app.route('/create')
def create_route():
    Bin.query.delete()
    BinData.query.delete()
    # Dummy data
    db.session.add(Bin(**{"id": 1, "location": "location 1", "fill_rate": 20}))
    db.session.add(Bin(**{"id": 2, "location": "location 2", "fill_rate": 30}))
    db.session.add(Bin(**{"id": 3, "location": "location 3", "fill_rate": 50}))

    db.session.add(BinData(
        **{
            "id": 1,
            "bin_id": 1,
            "date_time": datetime.now(),
            "fill_level": 30,
            "temperature": 30,
            "humidity": 25
        }
    ))
    db.session.add(BinData(
        **{
            "id": 2,
            "bin_id": 2,
            "date_time": datetime.now(),
            "fill_level": 46,
            "temperature": 33,
            "humidity": 20
        }
    ))
    db.session.add(BinData(
        **{
            "id": 3,
            "bin_id": 3,
            "date_time": datetime.now(),
            "fill_level": 99,
            "temperature": 35,
            "humidity": 27
        }
    ))
    db.session.add(BinData(
        **{
            "id": 4,
            "bin_id": 2,
            "date_time": datetime.now(),
            "fill_level": 79,
            "temperature": 38,
            "humidity": 22
        }
    ))
    db.session.add(BinData(
        **{
            "id": 5,
            "bin_id": 1,
            "date_time": datetime.now(),
            "fill_level": 60,
            "temperature": 38,
            "humidity": 26
        }
    ))


    db.session.commit()
    return "<a href='/view-db'>go</a>"