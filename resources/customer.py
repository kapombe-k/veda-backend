from flask import make_response, request
from flask_restful import Resource

from models import db, Customer


class Customers(Resource):
    def get(self):
        customers = Customer.query.all()

        customer_list = [customer.to_dict() for customer in customers]
        return make_response(customer_list, 200)
    
    def post(self):

        data = request.json()

        try:
            new_customer = Customer(
                username = data.get('username'),
                email = data.get('email'),
                phone = data.get('phone'),
                age = data.get('age'),
                address = data.get('address'),
                password = data.get('password'),
            )

            db.session.add(new_customer)
            db.session.commit()

            return make_response(new_customer.to_dict(), 201)
        
        except Exception:
            db.session.rollback()

            return make_response({'message': 'Error creating customer:', 'status': 500})
    
class CustomerbyId(Resource):

    def get(self, id):
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            response = {"message": "Customer not found", "status": 404}
            return make_response(response, 404)

        return make_response(customer.to_dict(), 200) 

    def patch(self, id):
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return make_response({"error": "Product not found"}, 404)

        data = request.get_json()

        try:
            customer.name = data.get("name", customer.name)
            customer.price = data.get("price", customer.price)
            customer.quantity = data.get("quantity", customer.quantity)
            customer.details = data.get("details", customer.details)
            customer.image = data.get("image", customer.image)
            customer.category = data.get("price", customer.category)
            customer.category_id = data.get("category_id", customer.category_id)

            db.session.commit()

            return make_response(customer.to_dict(), 200)

        except Exception as e:
            return make_response({"error": str(e)}, 400)

    def delete(self, id):
        customer = Customer.query.filter_by(id=id).first()

        if not customer:
            return make_response({"error": "customer not found"}, 404)

        db.session.delete(customer)
        db.session.commit()

        return make_response({"message": "customer deleted successfully"}, 200)
