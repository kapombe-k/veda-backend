from flask import request
from flask_restful import Resource
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from models import db, User
from datetime import timedelta

class Register(Resource):
    def post(self):
        data  = request.get_json()

        # validations for required fields for password
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields: username, email, password'}, 400

        email = User.query.filter_by(email=data.get("email")).first()

        if email:
            return {'message':'Email is already taken', 'status': 422}
    
        plaintext_password = data.get("password")
    
        hash = generate_password_hash(plaintext_password).decode('utf-8')

        del plaintext_password

        # add User
        new_user = User(
                username = data.get('username'),
                email = data.get('email'),
                phone = data.get('phone'),
                age = data.get('age'),
                address = data.get('address'),
                password = hash,
                role='customer' #added deault role from the table update
            )

        db.session.add(new_user)
        db.session.commit()

        # generate access token using jwt
        token = create_access_token(
            identity=new_user.id,
            additional_claims={'role':new_user.role},
            expires_delta=timedelta(hours=12)
        )

        return {
            'message':'Account created successfully',
            'access_token': token,
            'user': new_user.to_dict()
        }, 201
        

# signin renamed login for consistnecy       
        
    
class LogIn(Resource):
    def post(self):

        data = request.get_json()

        # add validations for required fields
        if not data or 'email' not in data or 'password' not in data:
            return {'message': 'Missing email or password'}, 400

        user = User.query.filter_by(email=data.get('email')).first()

        if user is None:
            return {'message':'Invalid e-mail or password'}, 403

        if not check_password_hash(user.password, data.get('password')):
            return {'message':'Invalid e-mail or password'}, 401 #refactored to remove else at the bottom
        
        token = create_access_token(identity=user.id)

        return {
                'message':'Login successful!',
                'user': user.to_dict(),
                'access_token': token
        }

