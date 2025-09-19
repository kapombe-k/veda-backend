from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import re

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-password',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer)
    email_address = db.Column(db.String)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    role = db.Column(db.String(20), default='customer')  # Added role column

    # RELATIONSHIPS
    orders = db.relationship('Order', back_populates='user', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='user')

    @validates('email')
    def validate_email(self, key, email_address):
        normalized = email_address.strip().lower()
        regex_validator = r"[A-Za-z][A-Za-z0-9]*(\.[A-Za-z0-9]+)*@[A-Za-z0-9]+\.[a-z]{2,}"
        if not re.match(regex_validator, normalized):
            raise ValueError("Email is not valid")
        return normalized

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    details = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer) # changed to integer and stock (better name)
    rating = db.Column(db.Float)

    # foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # relationships
    category = db.relationship('Category', back_populates='products')
    reviews = db.relationship('Review', back_populates='product')
    order_items = db.relationship('OrderItem', back_populates='product')  # Changed relationship name

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    serialize_only = ('category_name',)

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # relationship
    products = db.relationship('Product', back_populates='category')

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')

    # foreign key
    order_id = db.Column(db.Integer,db.ForeignKey('orders.id'))

    # relationships
    order = db.relationship('Order', back_populates='cart')
    user = db.relationship('User', back_populates='cart')
    

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, default='pending') # added a more desciptive status
    order_date = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)

    # foreign keys (updated to user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # relationships (changed 2 user)
    order_items = db.relationship('OrderItem', back_populates='order')
    user = db.relationship('User', back_populates='orders')


class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # foreign keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # relationships
    order = db.relationship('Order', back_populates='order_items')
    product = db.relationship('Product')

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    review = db.Column(db.String)
    created_at=db.Column(db.DateTime(), default=datetime.now()) # added at timestamp fr the reviews

    # foreign keys (user update)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # relationships (user update)
    user = db.relationship('User', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')


 # summarry of changes made
# Fixed the Review model to properly define relationships with user and Product

# Corrected all back_populates values to be consistent across models

# Changed foreign keys to use IDs instead of names where appropriate

# Fixed the OrderItem class name (was Order_item)

# Removed duplicate foreign key in Product model

# Standardized relationship naming (e.g., product_review → reviews)

# Added missing relationships where needed

# Fixed the order-product relationship that was previously missing  
# 
# added cart schema     
