import os
from flask import Flask
from flask_restful import Api
from flask_login import UserMixin

from utils.db import db
from utils.login_manager import login_manager

from resources.information import Information
from resources.user import User
from resources.users import Users
from resources.session import Session
from resources.driver import Driver
from resources.drivers import Drivers
from resources.order import Order
from resources.orders import Orders
from resources.route import Route
from resources.routes import Routes

from models.user import UserModel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'wasay'
api = Api(app)

db.init_app(app)

login_manager.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

api.add_resource(User, "/users/<int:id>") # 取得基本資料
api.add_resource(Users, "/users") # 註冊
api.add_resource(Driver, "/drivers/<int:id>") # 取得基本資料
api.add_resource(Drivers, "/drivers") # 註冊
api.add_resource(Session, "/session") # 登入、登出
api.add_resource(Orders, "/orders") # 訂單
api.add_resource(Order, "/orders/<int:id>") # 訂單
api.add_resource(Route, "/routes/<int:id>") # 路線
api.add_resource(Routes, "/routes") # 路線

if __name__ == '__main__':
    app.run(port=5000, debug=True)

