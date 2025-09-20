#!/usr/bin/env python3

from flask import Flask, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()
    if not Plant.query.first():
        db.session.add(Plant(name="Aloe", image="./images/aloe.jpg", price=11.50))
        db.session.commit()

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.order_by(Plant.id).all()
        return [p.to_dict() for p in plants], 200

    def post(self):
        data = request.get_json(silent=True)
        if not data:
            return {"error": "Expected JSON body."}, 400
        name = data.get("name")
        image = data.get("image")
        price = data.get("price")
        if not name:
            return {"error": "Field 'name' is required."}, 400
        plant = Plant(name=name, image=image, price=price)
        db.session.add(plant)
        db.session.commit()
        return plant.to_dict(), 201

class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get(id)
        if not plant:
            return {"error": "Plant not found"}, 404
        return plant.to_dict(), 200

api.add_resource(Plants, "/plants")
api.add_resource(PlantByID, "/plants/<int:id>")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
