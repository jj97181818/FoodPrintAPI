from flask import request, abort, jsonify
from flask_restful import Resource

from models.user import UserModel
from models.farmer import FarmerModel
from models.route import RouteModel
from models.order import OrderModel
from models.item import ItemModel
from utils.db import db

class Farmers(Resource):  
    # 獲得司機資料
    def get(self):
        result = []
        for farmer in FarmerModel.query.all():
            vegetables = []
            for item in ItemModel.query.filter_by(FarmerID=farmer.id).all():
                vegetables.append({"id":item.id, "vegeName": item.vegeName, "vegeQuantity": item.vegeQuantity, "vegePrice": item.vegePrice})
            result.append({"id":farmer.id, "username":farmer.username, "name":farmer.name, "email":farmer.email, "address":farmer.address, "cellphone":farmer.cellphone, "vegetables":vegetables})
        return result

    # 註冊
    def post(self):
        username = request.json.get('username')
        name = request.json.get('name')
        password = request.json.get('password')
        email = request.json.get('email')
        address = request.json.get('address')
        cellphone = request.json.get('cellphone')

        if username is None or password is None:
            abort(400)
        if FarmerModel.query.filter_by(username=username).first() is not None:
            abort(400)

        farmer = FarmerModel(username=username)
        farmer.name = name
        farmer.hash_password(password)
        farmer.email = email
        farmer.address = address
        farmer.cellphone = cellphone
        db.session.add(farmer)
        db.session.commit()
        
        response = jsonify({'username':username})
        response.status_code = 201
        return response

