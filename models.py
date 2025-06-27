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

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    serialize_rules = ('-password',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # RELATIONSHIPS
    orders = db.relationship('Order', back_populates='customer', cascade="all, delete-orphan")
    reviews = db.relationship('Review', back_populates='customer')

    @validates('email')
    def validate_email(self, key, address):
        normalized = address.strip().lower()
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
    quantity = db.Column(db.Boolean)
    rating = db.Column(db.Float)

    # foreign key
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # relationships
    category = db.relationship('Category', back_populates='products')
    reviews = db.relationship('Review', back_populates='product')
    orders = db.relationship('Order', back_populates='product')

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    serialize_only = ('category_name',)

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # relationship
    products = db.relationship('Product', back_populates='category')

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    order_date = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)

    # foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # relationships
    order_items = db.relationship('OrderItem', back_populates='order')
    customer = db.relationship('Customer', back_populates='orders')
    product = db.relationship('Product', back_populates='orders')

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

    # foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # relationships
    customer = db.relationship('Customer', back_populates='reviews')
    product = db.relationship('Product', back_populates='reviews')


 # summarry of changes made
# Fixed the Review model to properly define relationships with Customer and Product

# Corrected all back_populates values to be consistent across models

# Changed foreign keys to use IDs instead of names where appropriate

# Fixed the OrderItem class name (was Order_item)

# Removed duplicate foreign key in Product model

# Standardized relationship naming (e.g., product_review → reviews)

# Added missing relationships where needed

# Fixed the order-product relationship that was previously missing      
