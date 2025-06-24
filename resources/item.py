from flask import make_response, request
from flask_restful import Resource

from models import db, Order_item

class Items(Resource):
    def get_all_items(self):
        order_items = Order_item.query.all()

        order_items_list = [order_items.to_dict() for order_items in order_items]

        return make_response(order_items_list, 200)

    def get_item_by_id(self, id):
        order_item = Order_item.query.filter_by(id=id).first()

        if not order_item:
            response ={
                'message':'order_item not found',
                'status': 404
            }
            return make_response(response, 404)
        
        return make_response(order_item.to_dict(), 200)

    def delete_item():
        item = Order_item.query.filter_by(id=id).first()

        if not item:
            return make_response({"error": "item not found"}, 404)
        
        db.session.delete(item)
        db.session.commit()

        return make_response({"message": "item deleted successfully"}, 200)