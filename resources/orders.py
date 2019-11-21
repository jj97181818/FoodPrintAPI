from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.order import OrderModel
from models.user import UserModel
from models.farmer import FarmerModel
from utils.db import db

class Orders(Resource):
    # 取得所有訂單
    def get(self):
        result = []
        for order in OrderModel.query.all():
            location = order.location.split(",")
            farmer = FarmerModel.query.filter_by(id=order.FarmerID).first()
            print("order 的 UserID", order.UserID, "\n")

            user = UserModel.query.filter_by(id=order.UserID).first()
            loc = location[0] + "," + location[1]
            items = {"foodName":order.foodName, "farmerName":farmer.name, "farmerID":order.FarmerID, "foodQuantity":order.foodQuantity, "foodPrice":order.foodPrice}
            result.append({'id':order.id, 'status':order.status, 'profit':order.profit,'address':order.address, 'orderDate':order.orderDate, "userID":order.UserID, "userName": user.name, "userCellphone":user.cellphone, "location":loc, "items":items})
        return result

    # 上傳訂單
    def post(self):
        UserID = request.json.get('userID')
        status = request.json.get('status')
        profit = request.json.get('profit')
        orderDate = request.json.get('orderDate')
        address = request.json.get('address')
        location = request.json.get('location').get('latitude') + "," + request.json.get('location').get('latitude')
        foodName = request.json.get('items').get('foodName')
        farmerID = request.json.get('items').get('farmerID')
        foodQuantity = request.json.get('items').get('foodQuantity')
        foodPrice = request.json.get('items').get('foodPrice')
        
        if foodName is None:
            abort(400)

        order = OrderModel()
        order.UserID = UserID
        order.status = status
        order.profit = profit
        order.orderDate = orderDate
        order.address = address
        order.location = location
        order.FarmerID = farmerID
        order.foodName = foodName
        order.foodQuantity = foodQuantity
        order.foodPrice = foodPrice
    
        db.session.add(order)
        db.session.commit()
        
        response = jsonify({'id':order.id})
        response.status_code = 201
        return response

