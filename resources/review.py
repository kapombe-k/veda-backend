from flask import make_response, request
from flask_restful import Resource

from models import db, Review

class Reviews(Resource):
    def get_product_review():
        pass

    def update_product_review():
        product = Product.query.filter_by(id=id).first()

        if not product:
            return make_response({"error": "Product not found"}, 404)
        
        data = request.get_json()

        try:
            product.name = data.get('name', product.name)
            product.price = data.get('price', product.price)
            product.quantity = data.get('quantity', product.quantity)
            product.details = data.get('details', product.details)
            product.image = data.get('image', product.image)
            product.category = data.get('price', product.category)
            product.category_id = data.get('category_id', product.category_id)

            db.session.commit()

            return make_response(product.to_dict(), 200)
        
        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def delete_product_review():
        review = Review.query.filter_by(id=id).first()

        if not review:
            return make_response({"error": "review not found"}, 404)
        
        db.session.delete(review)
        db.session.commit()

        return make_response({"message": "review deleted successfully"}, 200)