from flask_restful import Resource, request
from flask import jsonify
from flask_login import UserMixin, login_user, logout_user

from models.user import UserModel
from models.driver import DriverModel

from utils.login_manager import User

class Session(Resource):
    # 登入
    def post(self):
        identity = request.json.get('identity')
        username = request.json.get('username')
        password = request.json.get('password')
        if identity == 'restaurant':
            user = UserModel.query.filter_by(username = username).first()
            ID = user.id
        elif identity == 'farmer':
            driver = DriverModel.query.filter_by(username = username).first()
            ID = driver.id

        if not user or not user.verify_password(password):
            return {"message":"Login failed!"}, 401
        else:
            login_user(User(username))

        return {"message":"Login successfully", "ID":ID}, 201

    # 登出
    def delete(self):
        logout_user()
        return {'message':'Logout successfully'}, 200