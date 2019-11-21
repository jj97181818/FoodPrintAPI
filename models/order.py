import datetime

from utils.db import db

class OrderModel(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key = True)
    arrivalTime = db.Column(db.String(100))
    orderDate = db.Column(db.String(100))
    status = db.Column(db.Integer)
    location = db.Column(db.String(100))
    address = db.Column(db.String(100))
    sequence = db.Column(db.Integer)

    foodName = db.Column(db.String(100))
    foodQuantity = db.Column(db.Float)
    foodPrice = db.Column(db.Float)
    profit = db.Column(db.Float)
    
    UserID = db.Column(db.Integer, db.ForeignKey('users.id'))
    FarmerID = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    RouteID = db.Column(db.Integer, db.ForeignKey('routes.id'))