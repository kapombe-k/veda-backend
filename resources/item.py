from flask import make_response, request
from flask_restful import Resource

from models import db, OrderItem

class Items(Resource):
    def get(self):
        order_items = OrderItem.query.all()

        order_items_list = [order_items.to_dict() for order_items in order_items]

        return make_response(order_items_list, 200)
    
class ItemsById(Resource):

    def get(self, id):
        order_item = OrderItem.query.filter_by(id=id).first()

        if not order_item:
            response ={
                'message':'order_item not found',
                'status': 404
            }
            return make_response(response, 404)
        
        return make_response(order_item.to_dict(), 200)
    
    def patch(self, id):
        order_item = OrderItem.query.filter_by(id=id).first()

        if not order_item:
            return make_response({"error": "order_item not found"}, 404)

        data = request.get_json()

        try:
            order_item.quantity = data.get("quantity", order_item.quantity)
            
            db.session.commit()

            return make_response(order_item.to_dict(), 200)

        except Exception:
            response = {
                "status": "failed",
                "code": 402,
                "message": "order_item not added successfully",
            }
            return make_response(response, 400)

    def delete(self, id):
        item = OrderItem.query.filter_by(id=id).first()

        if not item:
            return make_response({"error": "item not found"}, 404)
        
        try:
            db.session.delete(item)
            db.session.commit()

            response = {
                "status": "deleted",
                "code": 200,
                "message": "Item deleted",
            }

            return make_response(response, 200)

        except Exception:
            response = {
                "status": "failed",
                "code": 402,
                "message": "Failed to delete item",
            }

            db.session.rollback()

            return make_response(response, 400)