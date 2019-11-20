from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.item import ItemModel
from utils.db import db

class Item(Resource):
    def put(self, id):
        vegeName = request.json.get('vegeName')
        vegeQuantity = request.json.get('vegeQuantity')
        vegePrice = request.json.get('vegePrice')

        item = ItemModel.query.filter_by(id=id).first()
        if item is None:
            item = ItemModel(id)
            item.vegeName = vegeName
            item.vegeQuantity = vegeQuantity
            item.vegePrice = vegePrice
        else:
            item.vegeName = vegeName
            item.vegeQuantity = vegeQuantity
            item.vegePrice = vegePrice

        db.session.add(item)
        db.session.commit()
        return {"message":"Change successfully!"}

    def delete(self, id):
        item = ItemModel.query.filter_by(id=id).first()
        db.session.delete(item)
        db.session.commit()

        return {"message":"Delete successfully!"}