from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

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

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False) 
    email = db.Column(db.String, unique =True, nullable=False)
    phone = db.Column(db.Integer, unique =True, nullable =False )
    age = db.Column(db.Integer)
    address = db.Column(db.String)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    # RELATIONSHIPS
    orders = db.relationship('Orders', back_populates= 'customer', cascade="all, delete-orphan")
    customer_reviews = db.relationship('Review', back_populates='customer')


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

    # foreign keys
    category = db.Column(db.String, db.ForeignKey('categories.category_name'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    # relationship
    product_review = db.relationship('Review', back_populates = 'products')
    orders = db.relationship('Order', back_populates= 'product')

class Category(db.Model, SerializerMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())

    #relationship
    products = db.relationship('Product', back_populates= 'category')

class Order(db.Model,SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    order_date = db.Column(db.DateTime(), default=datetime.now(), nullable=False)
    total_amount =  db.Column(db.Integer, nullable=False)

    # foreign key
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # relationship
    order_items = db.relationship('Order_item', back_populates='order')
    customer = db.relationship('Customer', back_populates = 'order')


class Order_item(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    quantity = db.Column(db.Integer, nullable=False)

    # foreign key
    product_name = db.Column(db.String, db.ForeignKey('products.name') )
    # relationship
    order = db.relationship('Order', back_populates = 'order_item')

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    product_name = db.Column(db.Integer, db.ForeignKey('products.name'))
    review = db.Column(db.String)