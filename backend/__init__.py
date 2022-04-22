from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # we don't need real time updates as this is a REST based api
db = SQLAlchemy(app)

from backend.models import *
db.create_all()

@app.route('/')
def index():
    return render_template('index.html', **{
        "heading": "Smart Routing for Urban Waste Collection",
        "by": "Samridh"
    })