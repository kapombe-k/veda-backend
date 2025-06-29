from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, OrderItem, Order, User

class OrderItems(Resource):
    @jwt_required()
    def get(self):
        """Get all order items (admin only)"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            # Only admins can view all order items
            if user.role != 'admin':
                return make_response({'message': 'Admin access required'}, 403)
            
            order_items = OrderItem.query.all()
            return [item.to_dict() for item in order_items], 200
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)

class OrderItemById(Resource):
    @jwt_required()
    def get(self, id):
        """Get specific order item (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order_item = OrderItem.query.get_or_404(id)
            
            # Get the associated order
            order = Order.query.get(order_item.order_id)
            if not order:
                return make_response({'message': 'Order not found'}, 404)
            
            # Verify authorization
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({'message': 'Unauthorized access'}, 403)
            
            return make_response(order_item.to_dict(), 200)
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)
    
    @jwt_required()
    def patch(self, id):
        """Update order item quantity (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order_item = OrderItem.query.get_or_404(id)
            
            # Get the associated order
            order = Order.query.get(order_item.order_id)
            if not order:
                return make_response({'message': 'Order not found'}, 404)
                
            # Verify authorization
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({'message': 'Unauthorized access'}, 403)
            
            data = request.get_json()
            
            # Only allow quantity updates
            if 'quantity' in data:
                order_item.quantity = data['quantity']
                db.session.commit()
                return make_response(order_item.to_dict(), 200)
            else:
                return make_response({'message': 'No valid fields provided for update'}, 400)
                
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)
    
    @jwt_required()
    def delete(self, id):
        """Delete order item (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order_item = OrderItem.query.get_or_404(id)
            
            # Get the associated order
            order = Order.query.get(order_item.order_id)
            if not order:
                return make_response({'message': 'Order not found'}, 404)
                
            # Verify authorization (owner or admin)
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({
                        'message': 'Unauthorized - only order owner or admin can delete items'
                    }, 403)
            
            db.session.delete(order_item)
            db.session.commit()
            
            # Recalculate order total
            self.recalculate_order_total(order.id)
            
            return make_response({'message': 'Order item deleted successfully'}, 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 500)
    
    def recalculate_order_total(self, order_id):
        """Recalculate order total after item deletion"""
        order = Order.query.get(order_id)
        if order:
            total = 0
            for item in order.order_items:
                total += item.product.price * item.quantity
            order.total_amount = total
            db.session.commit()

class OrderItemsByOrder(Resource):
    @jwt_required()
    def get(self, order_id):
        """Get items for a specific order (order owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order = Order.query.get_or_404(order_id)
            
            # Verify authorization
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({'message': 'Unauthorized access'}, 403)
            
            order_items = OrderItem.query.filter_by(order_id=order_id).all()
            return [item.to_dict() for item in order_items], 200
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)