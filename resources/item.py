from flask import make_response, request
from flask_restful import Resource

from models import db, Order_item

class Items(Resource):
    def get_all_items():
        pass

    def get_item_by_id():
        pass

    def delete_item():
        item = Order_item.query.filter_by(id=id).first()

        if not item:
            return make_response({"error": "item not found"}, 404)
        
        db.session.delete(item)
        db.session.commit()

        return make_response({"message": "item deleted successfully"}, 200)