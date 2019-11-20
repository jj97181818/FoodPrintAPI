from flask import request, abort, jsonify
from flask_restful import Resource

from models.user import UserModel
from models.driver import DriverModel
from models.route import RouteModel
from models.order import OrderModel
from utils.db import db

class Drivers(Resource):  
    # 獲得司機資料
    def get(self):
        result = []
        for driver in DriverModel.query.all():
            route = RouteModel.query.filter_by(finish=0, DriverID=driver.id).first()
            user = UserModel.query.filter_by(username=driver.username).first()
            
            if route is None:
                result.append({"driverID":driver.id, "routeID":None, "name":user.name, "licensePlate":driver.licensePlate, "phone":user.cellphone, "dynamicAddress":driver.dynamicAddress, "dynamicLocation":driver.dynamicLocation, "finishedPercent":None})
                
            else:
                finishedNum = 0
                unfinishedNum = 0
                finishedPercent = 0

                for order in OrderModel.query.filter_by(RouteID=route.id).all():
                    if order.status == 2:
                        finishedNum += 1
                    elif order.status == 1:
                        unfinishedNum += 1
                finishedPercent = finishedNum / (finishedNum + unfinishedNum)

                result.append({"driverID":driver.id, "routeID":route.id, "name":user.name, "licensePlate":driver.licensePlate, "phone":user.cellphone, "dynamicAddress":driver.dynamicAddress, "dynamicLocation":driver.dynamicLocation, "finishedPercent":finishedPercent})
            return result

    # 註冊
    def post(self):
        username = request.json.get('username')
        licensePlate = request.json.get('licensePlate')
        carCapacity = request.json.get('carCapacity')
        dynamicAddress = request.json.get('dynamicAddress')
        dynamicLocation = request.json.get('dynamicLocation')

        if username is None or licensePlate is None or carCapacity is None:
            abort(400)
        if UserModel.query.filter_by(username=username).first() is None:
            abort(400)
            
        driver = DriverModel(username=username)
        driver.licensePlate = licensePlate
        driver.carCapacity = carCapacity
        driver.dynamicAddress = dynamicAddress
        driver.dynamicLocation = dynamicLocation
        db.session.add(driver)
        db.session.commit()
        
        response = jsonify({'username':username})
        response.status_code = 201
        return response
