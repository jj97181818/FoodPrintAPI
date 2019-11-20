import datetime

from utils.db import db

class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    arrivalTime = db.Column(db.String(100))
    status = db.Column(db.Integer)
    objectID = db.Column(db.Integer)
    weight = db.Column(db.Float)
    profit = db.Column(db.Float)
    location = db.Column(db.String(100))
    address = db.Column(db.String(100))
    sequence = db.Column(db.Integer)
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'))
    RouteID = db.Column(db.Integer, db.ForeignKey('routes.id'))