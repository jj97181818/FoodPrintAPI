from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from flask import current_app as app

from utils.db import db
from models.order import OrderModel

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    name = db.Column(db.String(32))
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(50))
    address = db.Column(db.String(100))
    cellphone = db.Column(db.String(15))
    latitude = db.Column(db.String(50))
    longitude = db.Column(db.String(50))

    order = db.relationship('OrderModel')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

