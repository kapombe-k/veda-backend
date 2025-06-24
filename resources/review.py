from flask import make_response, request
from flask_restful import Resource

from models import db, Review

class Reviews(Resource):
    def get_product_review():
        pass

    def post_review(self):

        data = request.json()

        try:
            new_review = Review(
                name = data.get('product_name'),
                user = data.get('user_id'),
                review = data.get('review')
            )

            db.session.add(new_review)
            db.session.commit()

            return make_response(new_review.to_dict(), 201)
        
        except Exception as e:
            response = {
                "status": "failed",
                "code": 402,
                "message": "product not added successfully",
            }
            return make_response(response, 400)
            
    def update_product_review():
        review = Review.query.filter_by(id=id).first()

        if not review:
            return make_response({"error": "review not found"}, 404)
        
        data = request.get_json()

        try:
            review.review = data.get('review', review.review)

            db.session.commit(review)

            return make_response(review.to_dict(), 200)
        
        except Exception:
            response = {
                "status": "failed",
                "code": 402,
                "message": "Review updated successfully",
            }
            return make_response(response, 400)

    def delete_product_review():
        review = Review.query.filter_by(id=id).first()

        if not review:
            return make_response({"error": "review not found"}, 404)
        
        db.session.delete(review)
        db.session.commit()

        return make_response({"message": "review deleted successfully"}, 200)