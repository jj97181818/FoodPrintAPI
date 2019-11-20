from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.order import OrderModel
from models.user import UserModel
from utils.db import db

class Orders(Resource):
    # 取得所有訂單
    def get(self):
        history = request.args.get('history')
        result = []
        if history == '1':
            for order in OrderModel.query.filter_by(status=2).all():
                location = order.location.split(",")
                user = UserModel.query.filter_by(id=order.UserID).first()
                result.append({'id':order.id, 'status':order.status, 'objectID':order.objectID, 'weight':order.weight, 'profit':order.profit, 'address':order.address, 'arrivalTime':order.arrivalTime, 'name':user.name, 'cellphone':user.cellphone, 'latitude': location[0], 'longitude': location[1]})
        elif history == '0':
            for order in OrderModel.query.all():
                location = order.location.split(",")
                user = UserModel.query.filter_by(id=order.UserID).first()
                result.append({'id':order.id, 'status':order.status, 'objectID':order.objectID, 'weight':order.weight, 'profit':order.profit, 'address':order.address, 'arrivalTime':order.arrivalTime, 'name':user.name, 'cellphone':user.cellphone, 'latitude': location[0], 'longitude': location[1]})
        return result

    # 上傳訂單
    def post(self):
        status = request.json.get('status')
        objectID = request.json.get('objectID')
        weight = request.json.get('weight')
        profit = request.json.get('profit')
        location = request.json.get('location')
        address = request.json.get('address')
        sequence = request.json.get('sequence')
        UserID = request.json.get('UserID')

        if objectID is None:
            abort(400)

        order = OrderModel()
        order.status = status
        order.objectID = objectID
        order.weight = weight
        order.profit = profit
        order.location = location
        order.address = address
        order.sequence = sequence
        order.UserID = UserID
        

        db.session.add(order)
        db.session.commit()
        
        response = jsonify({'id':order.id})
        response.status_code = 201
        return response

