from flask import make_response, request
from flask_restful import Resource

from models import db, Order

class Orders(Resource):
    def get_all_orders():
        orders = Order.query.all()

        orders_list = [orders.to_dict() for orders in orders]

        return make_response(orders_list, 200)

    def get_orders_by_customer_id(self, id):
        order_by_id = Order.query.filter(Order.user_id == id).all()

        if not order_by_id:
            response = {'message':'orders for this user not found', 'code':403}
            return make_response(response, 403)
        
        orders = [order.to_dict() for order in order_by_id]

        return make_response(orders.to_dict(), 200)

    def update_order():
        pass

    def delete_order(self, id):
        order = Order.query.filter_by(id=id).first()

        if not order:
            return make_response({"error": "order not found"}, 404)
        
        db.session.delete(order)
        db.session.commit()

        return make_response({"message": "order deleted successfully"}, 200)
    