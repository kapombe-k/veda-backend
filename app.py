from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

# Import all resources
from resources.auth import Register, LogIn
from resources.users import Users, UserById
from resources.product import Products, ProductById, AdminProducts, AdminProductById
from resources.category import Categories, CategoriesById
from resources.review import Reviews, ReviewById, ProductReviews, UserReviews
from resources.order import Orders, OrderById, OrderItems
from resources.item import OrderItems as OrderItemsResource, OrderItemById, OrderItemsByOrder

# Initialize Flask app
app = Flask(__name__)

# Configure JWT
app.config["JWT_SECRET_KEY"] = "your-very-secret-key"  # Change this in production!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 86400  # 24 hours in seconds

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Initialize API
api = Api(app)

@app.route('/')
def index():
    return "<h1>Welcome to Veda API</h1>"

# ======================
# Authentication Routes
# ======================
api.add_resource(Register, '/register')
api.add_resource(LogIn, '/login')

# =================
# User Routes
# =================
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')

# ==================
# Product Routes
# ==================
# Public routes
api.add_resource(Products, '/products')
api.add_resource(ProductById, '/products/<int:id>')

# Admin-only routes
api.add_resource(AdminProducts, '/admin/products')
api.add_resource(AdminProductById, '/admin/products/<int:id>')

# ===================
# Category Routes
# ===================
api.add_resource(Categories, '/categories')
api.add_resource(CategoriesById, '/categories/<int:id>')

# ==================
# Review Routes
# ==================
api.add_resource(Reviews, '/reviews')
api.add_resource(ReviewById, '/reviews/<int:id>')
api.add_resource(ProductReviews, '/products/<int:product_id>/reviews')
api.add_resource(UserReviews, '/user/reviews')

# =================
# Order Routes
# =================
api.add_resource(Orders, '/orders')
api.add_resource(OrderById, '/orders/<int:id>')
api.add_resource(OrderItems, '/orders/<int:order_id>/items')

# ======================
# Order Item Routes
# ======================
api.add_resource(OrderItemsResource, '/order_items')
api.add_resource(OrderItemById, '/order_items/<int:id>')
api.add_resource(OrderItemsByOrder, '/orders/<int:order_id>/items')

if __name__ == "__main__":
    app.run(port=5555, debug=True)