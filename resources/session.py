from flask_restful import Resource, request
from flask import jsonify
from flask_login import UserMixin, login_user, logout_user

from models.user import UserModel

from utils.login_manager import User

class Session(Resource):
    # 登入
    def post(self):
        platform = request.json.get('platform')
        username = request.json.get('username')
        password = request.json.get('password')
        if platform == 'app':
            user = UserModel.query.filter_by(username = username, permission = 0).first()
        elif platform == 'web':
            user = UserModel.query.filter_by(username = username, permission = 1).first()
        
        if not user or not user.verify_password(password):
            return {"message":"Login failed!"}, 401
        else:
            login_user(User(username))
        
        return {"message":"Login successfully"}, 201

    # 登出
    def delete(self):
        logout_user()
        return {'message':'Logout successfully'}, 200