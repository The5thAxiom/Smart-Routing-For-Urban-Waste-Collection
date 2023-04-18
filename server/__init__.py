from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, date

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api
db = SQLAlchemy(app)

from server.controllers import *
from server.models import *
db.create_all()

@app.route('/')
def index_route():
    return render_template('index.html', **{
        "heading": "Smart Routing for Urban Waste Collection",
    })

@app.route('/view-db')
def viewDB_route():
    return render_template('viewDb.html', ** {
        "bins": Bin.query.all(),
        "distances": Distances.query.all(),
        "binData": BinData.query.all()
    })

@app.route('/make-route')
def makeRoute_route():
    binsToCollect = getBinsToCollect()
    print(binsToCollect)
    bestPathById, graph, graphLabels = makeOptimalRoute(binsToCollect)
    return render_template('makeRoute.html',  ** {
        "bins": Bin.query.filter(
            Bin.id.in_(tuple(binsToCollect))
        ),
        "binData": BinData.query.filter(
            BinData.id.in_(tuple(binsToCollect))
        ),
        "graph": graph,
        "graphLabels": graphLabels,
        "route": bestPathById[:-1],
        "bins_to_collect": len(binsToCollect),
        "total_bins": len(BinData.query.all())
    })

from server import create_data