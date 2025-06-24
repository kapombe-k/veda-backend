from flask import make_response, request
from flask_restful import Resource

from models import db, Category

class Categories(Resource):
    def get_all_categories():
        pass

    def get_single_category(self, id):
        category = Category.query.filter_by(id=id).first()

    def update_category():
        category = Category.query.filter_by(id=id).first()

        if not category:
            return make_response({"error": "category not found"}, 404)
        
        data = request.get_json()

        try:
            category.name = data.get('category_name', category.name)

            db.session.commit()

            return make_response(category.to_dict(), 200)
        
        except Exception as e:
            return make_response({"error": str(e)}, 400)
        
    def get_products_in_category():
        category = Category.query.filter_by(id=id).first()

        if not category:
            return make_response({"error": "category not found"}, 404)
        
        db.session.delete(category)
        db.session.commit()

        return make_response({"message": "category deleted successfully"}, 200)