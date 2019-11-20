from flask import request, abort, jsonify
from flask_restful import Resource
import requests
from datetime import datetime

from models.route import RouteModel
from models.order import OrderModel
from models.farmer import FarmerModel
from models.user import UserModel
from utils.db import db
import config

class Routes(Resource):
    # 取得路線
    def get(self):
        # 資料從資料庫取得
        responses = []
        for route in RouteModel.query.filter_by(finish=0).all():
            orders = []
            finishedPercent = 0
            finishedOrderNum = 0
            OrderNum = 0
            for order in OrderModel.query.filter(OrderModel.RouteID==route.id, OrderModel.status!=0).all():
                if order.status == 1:
                    finish = 0
                elif order.status == 2:
                    finish = 1
                
                location = order.location.split(",")
                order = {
                    "orderSequence": order.sequence,
                    "orderID": order.id,
                    "orderAddress": order.address,
                    "arrivalTime": order.arrivalTime,
                    "finish": finish,
                    "latitude": location[0],
                    "longitude": location[1]
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
            responses.append(response)
        
        return {"routes":responses}


    # 創造路線
    def post(self):
        url = "https://api.likey.com.tw/1/usersequence.json?"
        date = request.json.get('date')
        
        item_unitprice = 5.5
        fuel_price = 3.2
        
        year, month, day = map(int, date.split('-'))
        date = datetime(year, month, day)

        # 從資料庫找出需要被安排進路線的訂單
        index = 1
        for order in OrderModel.query.filter_by(status=0).all():
            url += f"waypoint{index}={order.id};{order.location};{order.weight}&"
            index += 1
        
        url += f"departure=2019-08-07T09:30:00&mode=fastest;car;traffic:enabled;&target=mintime&item_unitprice={item_unitprice}&fuel_price={fuel_price}&app_id={config.APP_ID}&app_code={config.APP_CODE}"
        response = requests.get(url)
  
        # 資料存進資料庫
        for i in range(0, len(response.json()["results"][0]["waypoints"])): # 規劃出的路線數量
            route = RouteModel()
            route.finish = 0
            route.date = date
            db.session.add(route)
            db.session.commit()

            for j in range(0, len(response.json()["results"][0]["waypoints"][i])): # 路線的訂單數量
                print(i, " ", j)
                print("id: ", response.json()["results"][0]["waypoints"][i][j]["id"], " sequence: ", response.json()["results"][0]["waypoints"][i][j]["sequence"])
            
                orderID = response.json()["results"][0]["waypoints"][i][j]["id"]
                order = OrderModel.query.filter_by(id=orderID).first()
                order.status = 1
                order.sequence = response.json()["results"][0]["waypoints"][i][j]["sequence"]
                order.RouteID = route.id
                db.session.add(order)
                db.session.commit()
        
        return {"message":"Create new route(s) successfully."}