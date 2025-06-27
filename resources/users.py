from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, Customer

class Register(Resource):
    def post(self):

        data  = request.get_json()

        email = Customer.query.filter_by(email=data.get("email")).first()

        if email:
            return {'message':'Email is already taken', 'status': 422}
    
        password = Customer.query.filter_by(password=data.get("password"))
    
        hash = generate_password_hash(password).decode('utf-8')

        del password

        # add customer
        new_customer = Customer(
                username = data.get('username'),
                email = data.get('email'),
                phone = data.get('phone'),
                age = data.get('age'),
                address = data.get('address'),
                password = hash
            )

        db.session.add(new_customer)
        db.session.commit()

        # generate access token using jwt
        token = create_access_token(identity=new_customer.id)

        return {
            'message':'Account created successfully',
            'access_token': token,
            'user': new_customer.to_dict()
        }, 201
    
class SignIn(Resource):
    def post(self):

        data = request.get_json()

        user = Customer.query.filter_by(email=data.get('email')).first()

        if user is None:
            return {'message':'Invalid e-mail or password'}, 403

        if check_password_hash(user.password, data.get('password')):
            token = create_access_token(identity=user.id)

            return {
                'message':'Login successful!',
                'user': user.to_dict(),
                'access_token': token
            }
        else:
            return {'message':'Invalid email or password'}, 403
