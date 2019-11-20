from flask_restful import Resource
from flask import request

from models.user import UserModel
from models.farmer import FarmerModel
from models.item import ItemModel
from utils.db import db

class Farmer(Resource):
    # 取得基本資料
    def get(self, id):
        farmer = FarmerModel.query.filter_by(id=id).first()
        vegetables = []
        for item in ItemModel.query.filter_by(FarmerID=farmer.id).all():
            vegetables.append({"vegeName": item.vegeName, "vegeQuantity": item.vegeQuantity, "vegePrice": item.vegePrice})
        if farmer:
            return {"id":farmer.id, "username":farmer.username, "name":farmer.name, "email":farmer.email, "address":farmer.address, "cellphone":farmer.cellphone, "vegetables":vegetables}
        return {'message':'not found'}

    def put(self, id): 
        name = request.json.get('name')
        email = request.json.get('email')
        address = request.json.get('address')
        cellphone = request.json.get('cellphone')
        
        farmer = FarmerModel.query.filter_by(id=id).first()
        if farmer is None:
            farmer = FarmerModel(id)
        else:
            farmer.name = name
            farmer.email = email
            farmer.address = address
            farmer.cellphone = cellphone
     
        db.session.add(farmer)
        db.session.commit()
        return {"message":"Change successfully!"}

    def delete(self, id):
        farmer = FarmerModel.query.filter_by(id=id).first()
        db.session.delete(farmer)
        db.session.commit()

        return {"message":"Delete successfully!"}