from flask import make_response, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_bcrypt import generate_password_hash
from models import db, User

class Users(Resource):
    @jwt_required()
    def get(self):
        # Only admins can view all users
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user.role != 'admin':
            return make_response({'message': 'Admin access required'}, 403)
        
        users = User.query.all()
        return [user.to_dict() for user in users], 200

class UserById(Resource):
    @jwt_required()
    def get(self, id):
        current_user_id = get_jwt_identity()
        
        # Users can view their own profile, admins can view any
        if str(current_user_id) != str(id):
            current_user = User.query.get(current_user_id)
            if current_user.role != 'admin':
                return make_response({'message': 'Unauthorized access'}, 403)
        
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

    @jwt_required()
    def patch(self, id):
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Verify authorization
        if str(current_user_id) != str(id):
            current_user = User.query.get(current_user_id)
            if current_user.role != 'admin':
                return make_response({'message': 'Unauthorized access'}, 403)
        
        user = User.query.get_or_404(id)
        
        # Only admins can change roles
        if 'role' in data:
            if get_jwt().get('role') != 'admin':
                return make_response({'message': 'Admin privileges required'}, 403)
            user.role = data['role']
        
        # Update allowed fields
        allowed_fields = ['username', 'email', 'phone', 'age', 'address']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        # Handle password separately
        if 'password' in data:
            user.password = generate_password_hash(data['password'])
        
        db.session.commit()
        return user.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()
        
        # Only admins can delete users
        if get_jwt().get('role') != 'admin':
            return make_response({'message': 'Admin privileges required'}, 403)
        
        # Prevent self-deletion
        if str(current_user_id) == str(id):
            return make_response({'message': 'Cannot delete your own account'}, 400)
        
        user = User.query.get_or_404(id)
        
        db.session.delete(user)
        db.session.commit()
        return make_response({'message': 'User deleted successfully'}, 200)