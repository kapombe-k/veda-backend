from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Review, User, Product

class Reviews(Resource):
    #@jwt_required()
    def post(self):
        """Create a new review (authenticated users only)"""
        try:
            data = request.get_json()
            current_user_id = get_jwt_identity()
            
            # Validate required fields
            required_fields = ['product_id', 'review', 'rating']
            if not all(field in data for field in required_fields):
                return make_response({
                    "message": "Missing required fields: product_id, review, or rating"
                }, 400)
            
            # Check if product exists
            product = Product.query.get(data['product_id'])
            if not product:
                return make_response({"message": "Product not found"}, 404)
            
            # Create new review
            new_review = Review(
                user_id=current_user_id,
                product_id=data['product_id'],
                review=data['review'],
                rating=data['rating']
            )
            
            db.session.add(new_review)
            db.session.commit()
            
            return make_response(new_review.to_dict(), 201)
            
        except Exception:
            db.session.rollback()
            return make_response({
                "message": "Failed to create review"
            }, 400)

class ReviewById(Resource):
    #@jwt_required()
    def get(self, id):
        """Get a specific review by ID"""
        try:
            review = Review.query.get(id)
            
            if not review:
                return make_response({"message": "Review not found"}, 404)
                
            return make_response(review.to_dict(), 200)
            
        except Exception:
            return make_response({"message": "Review for product {id} found"}, 500)
    
    @jwt_required()
    def patch(self, id):
        """Update a review (only review owner)"""
        try:
            current_user_id = get_jwt_identity()
            review = Review.query.get(id)
            
            if not review:
                return make_response({"message": "Review not found"}, 404)
                
            # Verify ownership
            if review.user_id != current_user_id:
                return make_response({
                    "message": "Unauthorized - you can only edit your own reviews"
                }, 403)
                
            data = request.get_json()
            
            # Update allowed fields
            if 'review' in data:
                review.review = data['review']
            if 'rating' in data:
                review.rating = data['rating']
            
            db.session.commit()
            return make_response(review.to_dict(), 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Review cannot be updated"}, 400)
    
    @jwt_required()
    def delete(self, id):
        """Delete a review (owner or admin)"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            review = Review.query.get(id)
            
            if not review:
                return make_response({"message": "Review not found"}, 404)
                
            # Verify authorization (owner or admin)
            if review.user_id != current_user_id and user.role != 'admin':
                return make_response({
                    "message": "Unauthorized - only review owner or admin can delete"
                }, 403)
                
            db.session.delete(review)
            db.session.commit()
            
            return make_response({"message": "Review deleted successfully"}, 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({"message": "Review could not be deleted"}, 500)

class ProductReviews(Resource):
    def get(self, product_id):
        """Get all reviews for a specific product (public)"""
        try:
            reviews = Review.query.filter_by(product_id=product_id).all()
            return [review.to_dict() for review in reviews], 200
            
        except Exception as e:
            return make_response({"message": "Cannot get reviews"}, 500)

class UserReviews(Resource):
    @jwt_required()
    def get(self):
        """Get authenticated user's reviews"""
        try:
            current_user_id = get_jwt_identity()
            reviews = Review.query.filter_by(user_id=current_user_id).all()
            return [review.to_dict() for review in reviews], 200
            
        except Exception as e:
            return make_response({"message": str(e)}, 500)