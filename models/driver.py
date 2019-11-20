from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app as app
from utils.db import db

class DriverModel(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    licensePlate = db.Column(db.String(15))
    carCapacity = db.Column(db.Float)
    dynamicAddress = db.Column(db.String(100))
    dynamicLocation = db.Column(db.String(100))