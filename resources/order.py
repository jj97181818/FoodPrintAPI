from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.order import OrderModel
from utils.db import db

class Order(Resource):
    def delete(self, id):
        order = OrderModel.query.filter_by(id=id).first()
        db.session.delete(order)
        db.session.commit()

        return {"message":"Delete successfully!"}