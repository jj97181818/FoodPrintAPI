from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.order import OrderModel
from utils.db import db

class Order(Resource):
    # 取得單一訂單
    def get(self, id):
        order = OrderModel.query.filter_by(id=id).first()
        if order:
            location = order.location.split(",")
            return {'id':order.id, 'arrivalTime':order.arrivalTime, 'status':order.status, 'objectID':order.objectID, 'weight':order.weight, 'profit':order.profit, 'location':order.location, 'address':order.address, 'sequence':order.sequence, 'UserID':order.UserID, 'latitude': location[0], 'longitude': location[1]}
        return {'message':'not found'}
    
    def put(self, id): 
        status = request.json.get('status')
        objectID = request.json.get('objectID')
        weight = request.json.get('weight')
        profit = request.json.get('profit')
        location = request.json.get('location')
        address = request.json.get('address')

        order = OrderModel.query.filter_by(id=id).first()
        if order is None:
            order = OrderModel(id)
        else:
            order.status = status
            order.objectID = objectID
            order.weight = weight
            order.profit = profit
            order.location = location
            order.address = address

        db.session.add(order)
        db.session.commit()
        return {"message":"Change successfully!"}

    def delete(self, id):
        order = OrderModel.query.filter_by(id=id).first()
        db.session.delete(order)
        db.session.commit()

        return {"message":"Delete successfully!"}