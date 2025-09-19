from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Cart

class CartResource(Resource):
    @jwt_required()
    def get(self):
        """Endpoint to get all items in the cart"""
        try:
            user_id = get_jwt_identity()
            cart_items = Cart.query.filter_by(user_id=user_id).all()
            return make_response([item.to_dict() for item in cart_items], 200)
        except Exception:
            return make_response({'message': 'Could not retrieve cart items'}, 500)

    @jwt_required()    
    def post(self):
        """Endpoint to add an item to the cart"""
        try:
            data = request.get_json()
            new_cart_item = Cart(
                user_id=data.get('user_id'),
                status=data.get('status', 'pending'),
                order_id=data.get('order_id')
            )
            db.session.add(new_cart_item)
            db.session.commit()
            return make_response(new_cart_item.to_dict(), 201)
        except Exception:
            db.session.rollback()
            return make_response({'message': 'Could not add item to cart'}, 400)
        
    @jwt_required()
    def delete(self, id):
        """Endpoint to delete a cart"""
        try:
            cart_item = Cart.query.filter_by(id=id).first()
            if not cart_item:
                return make_response({'message': 'Cart item not found'}, 404)
            db.session.delete(cart_item)
            db.session.commit()
            return make_response({'message': 'Cart item deleted successfully'}, 200)
        except Exception:
            db.session.rollback()
            return make_response({'message': 'Could not delete cart item'}, 400)