from flask_restful import Resource
from flask import request

from models.user import UserModel
from utils.db import db

class User(Resource):
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first()
        if user:
            location = {"latitude":user.latitude, "longitude":user.longitude}
            return {'username':user.username, 'name':user.name, 'cellphone':user.cellphone, 'address':user.address, 'location':location, 'email':user.email}
        return {'message':'not found'}
    
    def put(self, id): 
        name = request.json.get('name')
        email = request.json.get('email')
        address = request.json.get('address')
        cellphone = request.json.get('cellphone')
        latitude = request.json.get('location').get('latitude')
        longitude = request.json.get('location').get('longitude')

        user = UserModel.query.filter_by(id=id).first()
        if user is None:
            user = UserModel(id)
        else:
            user.name = name
            user.email = email
            user.address = address
            user.cellphone = cellphone
            user.latitude = latitude
            user.longitude = longitude
     
        db.session.add(user)
        db.session.commit()
        return {"message":"Change successfully!"}

    def delete(self, id):
        user = UserModel.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()

        return {"message":"Delete successfully!"}