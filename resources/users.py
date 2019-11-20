from flask import request, abort, jsonify, g
from flask_restful import Resource

from models.user import UserModel
from utils.db import db

class Users(Resource):
    # 取得所有使用者
    def get(self):
        result = []
        for user in UserModel.query.all():
            result.append({'id':user.id, "username":user.username, "name":user.name, "email":user.email, "address":user.address, "cellphone":user.cellphone})
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
        if UserModel.query.filter_by(username=username).first() is not None:
            abort(400)

        user = UserModel(username=username)
        user.name = name
        user.hash_password(password)
        user.email = email
        user.address = address
        user.cellphone = cellphone

        db.session.add(user)
        db.session.commit()
        
        response = jsonify({'username':username})
        response.status_code = 201
        return response
