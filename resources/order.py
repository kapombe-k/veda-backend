from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, User, Product

class Orders(Resource):
    @jwt_required()
    def get(self):
        """Get orders for the current user"""
        try:
            current_user_id = get_jwt_identity()
            orders = Order.query.filter_by(user_id=current_user_id).all()
            return [order.to_dict() for order in orders], 200
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)
    
    @jwt_required()
    def post(self):
        """Create a new order for the current user"""
        try:
            current_user_id = get_jwt_identity()
            data = request.get_json()
            
            # Create new order
            new_order = Order(
                user_id=current_user_id,
                status='pending',
                total_amount=0  # Will be calculated
            )
            db.session.add(new_order)
            db.session.flush()  # Get order ID
            
            # Add order items
            total = 0
            for item in data['items']:
                # Create order item
                order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
                db.session.add(order_item)
                
                # Update total
                product = Product.query.get(item['product_id'])
                total += product.price * item['quantity']
            
            # Set calculated total
            new_order.total_amount = total
            db.session.commit()
            
            return make_response(new_order.to_dict(), 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)

class OrderById(Resource):
    @jwt_required()
    def get(self, id):
        """Get specific order (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order = Order.query.get_or_404(id)
            
            # Verify authorization
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({'message': 'Unauthorized access'}, 403)
            
            return make_response(order.to_dict(), 200)
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)
    
    @jwt_required()
    def patch(self, id):
        """Update order status (admin only)"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            # Only admins can update order status
            if user.role != 'admin':
                return make_response({'message': 'Admin access required'}, 403)
            
            order = Order.query.get_or_404(id)
            data = request.get_json()
            
            # Update status
            if 'status' in data:
                order.status = data['status']
                db.session.commit()
                return make_response(order.to_dict(), 200)
            else:
                return make_response({'message': 'No status provided'}, 400)
                
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)
    
    @jwt_required()
    def delete(self, id):
        """Delete entire order (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            order = Order.query.get_or_404(id)
            
            # Verify authorization (owner or admin)
            if str(order.user_id) != str(current_user_id):
                user = User.query.get(current_user_id)
                if user.role != 'admin':
                    return make_response({
                        'message': 'Unauthorized - only order owner or admin can delete'
                    }, 403)
            
            # Delete associated order items first
            OrderItem.query.filter_by(order_id=id).delete()
            
            # Delete the order
            db.session.delete(order)
            db.session.commit()
            
            return make_response({'message': 'Order deleted successfully'}, 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 500)

class OrderItems(Resource):
    @jwt_required()
    def post(self, order_id):
        """Add item to order (owner only)"""
        try:
            current_user_id = get_jwt_identity()
            order = Order.query.get_or_404(order_id)
            
            # Verify authorization
            if str(order.user_id) != str(current_user_id):
                return make_response({
                    'message': 'Unauthorized - only order owner can add items'
                }, 403)
                
            data = request.get_json()
            
            # Create new order item
            new_item = OrderItem(
                order_id=order_id,
                product_id=data['product_id'],
                quantity=data['quantity']
            )
            db.session.add(new_item)
            
            # Update order total
            product = Product.query.get(data['product_id'])
            order.total_amount += product.price * data['quantity']
            
            db.session.commit()
            return make_response(new_item.to_dict(), 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)