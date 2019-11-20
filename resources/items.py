from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.item import ItemModel
from models.user import UserModel

from utils.db import db

class Items(Resource):
    # 上傳訂單
    def post(self):
        vegeName = request.json.get('vegeName')
        vegeQuantity = request.json.get('vegeQuantity')
        vegePrice = request.json.get('vegePrice')
        FarmerID = request.json.get('FarmerID')

        item = ItemModel()
        item.vegeName = vegeName
        item.vegeQuantity = vegeQuantity
        item.vegePrice = vegePrice
        item.FarmerID = FarmerID
        
        db.session.add(item)
        db.session.commit()
        
        response = jsonify({'id':item.id})
        response.status_code = 201
        return response

