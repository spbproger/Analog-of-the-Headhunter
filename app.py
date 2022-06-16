import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///homework1.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        return jsonify([user.to_dict() for user in User.query.all()])

    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.close()
        return "Пользователь добавлен в базу данных", 200


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_one_user(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        if user is None:
            return "Пользователя с таким id не найдено"
        else:
            return jsonify(user.to_dict())

    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(uid)
        if user is None:
            return "Пользователь не найден", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.age = user_data['age']
        user.email = user_data['email']
        user.role = user_data['role']
        user.phone = user_data['phone']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {uid} успешно изменен", 200

    elif request.method == 'DELETE':
        user = db.session.query(User).get(uid)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {uid} успешно удален", 200


@app.route('/orders', methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'GET':
        return jsonify([order.to_dict() for order in Order.query.all()])

    if request.method == 'POST':
        try:
            order = json.loads(request.data)
            month_start, day_start, year_start = order['start_date'].split("/")
            month_end, day_end, year_end = order['end_date'].split("/")
            new_order_obj = Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
                end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id']
            )
            db.session.add(new_order_obj)
            db.session.commit()
            db.session.close()
            return "Заказ создан в базе данных", 200
        except Exception as e:
            return e


@app.route('/orders/<int:oid>', methods=['GET', 'PUT', 'DELETE'])
def get_one_order(oid):
    if request.method == 'GET':
        order = Order.query.get(oid)
        if order is None:
            return "Заказ с таким id не найден"
        else:
            return jsonify(order.to_dict())


@app.route('/offers', methods=['GET', 'POST'])
def get_all_offers():
    if request.method == 'GET':
        return jsonify([offer.to_dict() for offer in Offer.query.all()])

    if request.method == 'POST':
        offer = json.loads(request.data)
        new_offer_obj = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано в базе данных", 200


@app.route('/offers/<int:of_id>', methods=['GET', 'PUT', 'DELETE'])
def get_one_offer(of_id):
    if request.method == 'GET':
        offer = Offer.query.get(of_id)
        if offer is None:
            return "Предложение с таким id не найдено"
        else:
            return jsonify(offer.to_dict())


if __name__ == '__main__':
    app.run()
