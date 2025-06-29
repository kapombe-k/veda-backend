from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from models import db, Category

class Categories(Resource):
    def get(self):
        """Get all categories (public)"""
        try:
            categories = Category.query.all()
            return [category.to_dict() for category in categories], 200
        except Exception as e:
            return make_response({'message': str(e)}, 500)

    @jwt_required()
    def post(self):
        """Create new category (admin only)"""
        try:
            # Verify admin privileges
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return make_response({'message': 'Admin access required'}, 403)
            
            data = request.get_json()
            
            # Validate required field
            if 'category_name' not in data:
                return make_response({'message': 'Missing category_name'}, 400)
            
            # Check for duplicate category
            if Category.query.filter_by(category_name=data['category_name']).first():
                return make_response({'message': 'Category already exists'}, 409)
            
            new_category = Category(
                category_name=data['category_name']
            )
            
            db.session.add(new_category)
            db.session.commit()
            
            return make_response(new_category.to_dict(), 201)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)

class CategoriesById(Resource):
    def get(self, id):
        """Get specific category (public)"""
        try:
            category = Category.query.get(id)
            
            if not category:
                return make_response({'message': 'Category not found'}, 404)
                
            return make_response(category.to_dict(), 200)
            
        except Exception as e:
            return make_response({'message': str(e)}, 500)

    @jwt_required()
    def patch(self, id):
        """Update category (admin only)"""
        try:
            # Verify admin privileges
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return make_response({'message': 'Admin access required'}, 403)
            
            category = Category.query.get_or_404(id)
            data = request.get_json()
            
            # Update category name
            if 'category_name' in data:
                # Check for duplicate name
                if Category.query.filter(
                    Category.category_name == data['category_name'],
                    Category.id != id
                ).first():
                    return make_response({'message': 'Category name already exists'}, 409)
                    
                category.category_name = data['category_name']
                db.session.commit()
                return make_response(category.to_dict(), 200)
            else:
                return make_response({'message': 'No valid fields provided'}, 400)
                
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 400)

    @jwt_required()
    def delete(self, id):
        """Delete category (admin only)"""
        try:
            # Verify admin privileges
            claims = get_jwt()
            if claims.get('role') != 'admin':
                return make_response({'message': 'Admin access required'}, 403)
            
            category = Category.query.get_or_404(id)
            
            db.session.delete(category)
            db.session.commit()
            
            return make_response({'message': 'Category deleted successfully'}, 200)
            
        except Exception as e:
            db.session.rollback()
            return make_response({'message': str(e)}, 500)