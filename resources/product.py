from flask import make_response, request
from flask_restful import Resource

from models import db, Product

class Products(Resource):
    def get_all_products(self):

        products = Product.query.all()

        product_list = [product.to_dict() for product in products]

        return make_response(product_list, 200)
            

    def get_single_product(self, id):

        product = Product.query.filter_by(id=id).first()

        if not product:
            return {'message':'Product not found'}
        else: 
            return product.to_dict()
        
        

    def post_product():
        data = request.get_json()
        try:
            new_product = Product(
                name=data.get('name'),
                img=data.get('image'),
                details=data.get('details'),
                price=data.get('price'),
                quantity=data.get('quantity'),
                rating=data.get('rating'),
                category=data.get('category'),
                category_id=data.get('category_id')
            )
            db.session.add(new_product)
            db.session.commit()

            return make_response(new_product.to_dict(), 201)
        except Exception:
            response = {
                "status": "failed",
                "code": 402,
                "message": "product not added successfully",
            }
            return make_response(response, 400)

        

    def update_product(self, id):

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
        
        except Exception:
            response = {
                "status": "failed",
                "code": 402,
                "message": "product not added successfully",
            }
            return make_response(response, 400)

    def delete_product(self, id):
        product = Product.query.filter_by(id=id).first()

        if not product:
            return make_response({"error": "Product not found"}, 404)
        
        db.session.delete(product)
        db.session.commit()

        return make_response({"message": "Product deleted successfully"}, 200)
