from flask import make_response, request
from flask_restful import Resource

from models import db, Customer

class Customers(Resource):
    def get_all_customers(self):
        
        customers = Customer.query.all()

        return customers

    def get_customer_by_id(self, id):
        
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            response ={
                'message':'Customer not found',
                'status': 404
            }
            return make_response(response, 404)
        
        return make_response(customer.to_dict(), 200)

    def update_customer():
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return make_response({"error": "Product not found"}, 404)
        
        data = request.get_json()

        try:
            customer.name = data.get('name', customer.name)
            customer.price = data.get('price', customer.price)
            customer.quantity = data.get('quantity', customer.quantity)
            customer.details = data.get('details', customer.details)
            customer.image = data.get('image', customer.image)
            customer.category = data.get('price', customer.category)
            customer.category_id = data.get('category_id', customer.category_id)

            db.session.commit()

            return make_response(customer.to_dict(), 200)
        
        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def delete_customer():
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return make_response({"error": "customer not found"}, 404)
        
        db.session.delete(customer)
        db.session.commit()

        return make_response({"message": "customer deleted successfully"}, 200)
    