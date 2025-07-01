from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from .decorators import admin_required  # We'll need to createreference this to apply jwt admin authentication
from models import db, Product

class Products(Resource):
    def get(self):
        """Public endpoint to get all products"""
        try:
            products = Product.query.all()
            return [product.to_dict() for product in products], 200
        except Exception:
            return make_response({'message':'Cannot find products'}, 500)

class ProductById(Resource):
    def get(self, id):
        """Public endpoint to get a specific product"""
        try:
            # Changed to filter by ID instead of name
            product = Product.query.filter_by(id=id).first()
            
            if not product:
                return make_response({'message': 'Product not found'}, 404)
                
            return make_response(product.to_dict(), 200)
        except Exception as e:
            return make_response({'message': 'Product not found'}, 500)

class AdminProducts(Resource):
    @jwt_required()
    @admin_required
    def post(self):
        """Admin-only endpoint to create a new product"""
        try:
            data = request.get_json()
            
            # Create new product
            new_product = Product(
                name=data.get("name"),
                image=data.get("image"),  # Fixed field name
                details=data.get("details"),
                price=data.get("price"),
                stock=data.get("stock"),  # Changed from quantity to stock
                category_id=data.get("category_id"),
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            return make_response(new_product.to_dict(), 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': 'Error creating product.'}, 400)

class AdminProductById(Resource):
    @jwt_required()
    @admin_required
    def patch(self, id):
        """Admin-only endpoint to update a product"""
        try:
            product = Product.query.filter_by(id=id).first()
            
            if not product:
                return make_response({'message': 'Product not found'}, 404)
                
            data = request.get_json()
            
            # Update allowed fields
            allowed_fields = ['name', 'price', 'stock', 'image', 'details', 'category_id']
            for field in allowed_fields:
                if field in data:
                    setattr(product, field, data[field])
            
            db.session.commit()
            return make_response(product.to_dict(), 200)
            
        except Exception:
            db.session.rollback()
            return make_response({'message': 'Product could not be added'}, 400)

    @jwt_required()
    @admin_required
    def delete(self, id):
        """Admin-only endpoint to delete a product"""
        try:
            product = Product.query.filter_by(id=id).first()
            
            if not product:
                return make_response({'message': 'Product not found'}, 404)
                
            db.session.delete(product)
            db.session.commit()
            
            return make_response({'message': 'Product deleted successfully'}, 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': 'Product could not be deleted'}, 500)