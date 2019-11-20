from flask_restful import Resource
from flask import request

from models.user import UserModel
from models.driver import DriverModel
from utils.db import db

class Driver(Resource):
    # 取得基本資料
    def get(self, id):
        driver = DriverModel.query.filter_by(id=id).first()
        user = UserModel.query.filter_by(username=driver.username).first()
        if driver:
            return {'username':user.username, 'cellphone':user.cellphone, 'address':user.address, 'email':user.email, 'licensePlate':driver.licensePlate, 'carCapacity':driver.carCapacity, 'dynamicAddress':driver.dynamicAddress, 'dynamicLocation':driver.dynamicLocation}
        return {'message':'not found'}

    def put(self, id): 
        licensePlate = request.json.get('licensePlate')
        carCapacity = request.json.get('carCapacity')
        dynamicAddress = request.json.get('dynamicAddress')
        dynamicLocation = request.json.get('dynamicLocation')

        driver = DriverModel.query.filter_by(id=id).first()
        if driver is None:
            driver = DriverModel(id)
        else:
            driver.licensePlate = licensePlate
            driver.carCapacity = carCapacity
            driver.dynamicAddress = dynamicAddress
            driver.dynamicLocation = dynamicLocation
     
        db.session.add(driver)
        db.session.commit()
        return {"message":"Change successfully!"}

    def delete(self, id):
        driver = DriverModel.query.filter_by(id=id).first()
        db.session.delete(driver)
        db.session.commit()

        return {"message":"Delete successfully!"}