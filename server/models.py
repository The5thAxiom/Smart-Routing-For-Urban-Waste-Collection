from server import db

class Bin(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    location = db.Column(db.String, unique=False, nullable=False)
    fill_rate = db.Column(db.String, unique=False, nullable=False)
    bin_data = db.relationship('BinData', backref='bin', lazy=True)

class BinData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bin_id = db.Column(db.Integer, db.ForeignKey("bin.id"), nullable=False)
    date_time = db.Column(db.DateTime, nullable=True)
    fill_level = db.Column(db.Integer, unique=False, nullable=False)
    temperature = db.Column(db.Integer, unique=False, nullable=False)
    humidity = db.Column(db.Integer, unique=False, nullable=False)