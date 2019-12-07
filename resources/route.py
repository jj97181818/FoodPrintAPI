from flask import request, abort, jsonify
from flask_restful import Resource
import requests

from models.route import RouteModel
from models.order import OrderModel
from models.farmer import FarmerModel
from models.user import UserModel
from utils.db import db
import config

class Route(Resource):
    # 取得路線
    def get(self, id):
        route = RouteModel.query.filter_by(id=id).first()
        if route:
            orders = []
            finishedPercent = 0
            finishedOrderNum = 0
            OrderNum = 0

            for order in OrderModel.query.filter(OrderModel.RouteID==route.id, OrderModel.status!=0).all():
                if order.status == 1:
                    finish = 0
                elif order.status == 2:
                    finish = 1
                
                user = UserModel.query.filter_by(id=order.UserID).first()
                order = {
                    "orderSequence": order.sequence,
                    "orderID": order.id,
                    "orderAddress": order.address,
                    "arrivalTime": order.arrivalTime,
                    "finish": finish,
                    "latitude": user.latitude,
                    "longitude": user.longitude
                }
                orders.append(order)

                OrderNum += 1
                if finish == 1:
                    finishedOrderNum += 1
            finishedPercent = finishedOrderNum / OrderNum * 100
        
            response = {
                "routeID": route.id,
                "farmerID": route.FarmerID,
                "date": route.date,
                "totalProfit": route.totalProfit,
                "cost": route.cost,
                "finishedPercent": finishedPercent,
                "orders": orders
            }
        
            return {"route":response}
        return {'message':'not found'}

    def put(self, id):
        FarmerID = request.json.get('FarmerID')
        item_unitprice = 0
        fuel_price = 0
        
        # call routing API with farmer
        farmer = FarmerModel.query.filter_by(id=FarmerID).first()
        
        url = f"https://api.likey.com.tw/1/driverroute.json?driver={farmer.name};{farmer.latitude},{farmer.longitude};10&"

        index = 0
        for order in OrderModel.query.filter_by(RouteID=id).order_by(OrderModel.sequence.asc()).all():
            url += f"waypoint{index + 1}={order.id};{farmer.latitude},{farmer.longitude};{order.foodQuantity}&"
            index += 1
        
        url += f"departure=2019-08-07T09:30:00&mode=fastest;car;traffic:enabled;&target=mintime&item_unitprice={item_unitprice}&fuel_price={fuel_price}&app_id={config.APP_ID}&app_code={config.APP_CODE}"
        response = requests.get(url)
        
        route = RouteModel.query.filter_by(FarmerID=None).first()
        route.totalProfit = response.json()["results"][0]["total_profit"]
        route.cost = response.json()["results"][0]["total_fuel_consumption"] * fuel_price
        route.FarmerID = FarmerID
        db.session.add(route)
        db.session.commit()

        for i in range(1, len(response.json()["results"][0]["waypoints"])):
            orderID = response.json()["results"][0]["waypoints"][i]["id"]
            order = OrderModel.query.filter_by(id=orderID).first()
            order.arrivalTime = response.json()["results"][0]["waypoints"][i]["estimatedArrival"]
            order.sequence = int(response.json()["results"][0]["waypoints"][i]["sequence"])
            db.session.add(order)
            db.session.commit()
        
        return {"message":"Change successfully!"}
    
    def delete(self, id):
        route = RouteModel.query.filter_by(id=id).first()
        db.session.delete(route)
        db.session.commit()

        return {"message":"Delete successfully!"}