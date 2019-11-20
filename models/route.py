from utils.db import db

class RouteModel(db.Model):
    __tablename__ = 'routes'
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String)
    finish = db.Column(db.Integer)
    cost = db.Column(db.Float)
    totalProfit = db.Column(db.Float)
    jsonData = db.Column(db.JSON)
    DriverID = db.Column(db.Integer)
