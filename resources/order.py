from flask import make_response, request
from flask_restful import Resource

from models import db, Order

class Orders(Resource):
    def get_all_orders():
        pass

    def get_order_by_customer_id():
        pass

    def update_order():
        pass

    def delete_order():
        order = Order.query.filter_by(id=id).first()

        if not order:
            return make_response({"error": "order not found"}, 404)
        
        db.session.delete(order)
        db.session.commit()

        return make_response({"message": "order deleted successfully"}, 200)
    