#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    all_bakeries=[]
    for bakery in Bakery.query.all():
        bakery_dict = bakery.to_dict()
        all_bakeries.append(bakery_dict)

    response = make_response(jsonify(all_bakeries), 200)
    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()

    bakery_dict = bakery.to_dict()

    response = make_response(jsonify(bakery_dict), 200)

    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    price_list = []
    baked_goods = BakedGood.query.order_by(BakedGood.price).all()

    for baked_good in baked_goods:
        baked_goods_dict = baked_good.to_dict()
        price_list.append(baked_goods_dict)

    response = make_response(jsonify(price_list), 200)

    response.headers["Content-Type"] = "application/json"

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    baked_goods_dict = baked_goods.to_dict()
    response = make_response(jsonify(baked_goods_dict), 200)

    response.headers["Content-Type"] = "application/json"

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
