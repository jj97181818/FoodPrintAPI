from utils.db import db

class ItemModel(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    vegeName = db.Column(db.String(100))
    vegeQuantity = db.Column(db.Integer)
    vegePrice = db.Column(db.Integer)
    FarmerID = db.Column(db.Integer, db.ForeignKey('farmers.id'))
    
    