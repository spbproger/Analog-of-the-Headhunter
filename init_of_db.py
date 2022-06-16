import datetime
import sp_info
from models import *

db.drop_all()

db.create_all()

for user in sp_info.USERS:
    db.session.add(User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone'],
    ))

for order in sp_info.ORDERS:
    month_st, day_st, year_st = order['start_date'].split('/')
    month_en, day_en, year_en = order['end_date'].split('/')
    db.session.add(Order(
        id=order['id'],
        name=order['name'],
        description=order['description'],
        start_date=datetime.date(year=int(year_st), month=int(month_st), day=int(day_st)),
        end_date=datetime.date(year=int(year_en), month=int(month_en), day=int(day_en)),
        address=order['address'],
        price=order['price'],
        customer_id=order['customer_id'],
        executor_id=order['executor_id'],
    ))


for offer in sp_info.OFFERS:
    db.session.add(Offer(
        id=offer['id'],
        order_id=offer['order_id'],
        executor_id=offer['executor_id'],
    ))

db.session.commit()