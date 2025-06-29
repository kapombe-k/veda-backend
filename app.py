from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from models import db


from resources.category import Categories, CategoriesById
from resources.item import Items, ItemsById
from resources.order import Orders, OrderById
from resources.review import Reviews, ReviewsById
from resources.product import Products, ProductById
from resources.auth import Register, LogIn



# we initiate the flask app
app = Flask(__name__)

# bcrypt extension is imported for the flask object here.
bcrypt = Bcrypt(app)

# let's connect the database using the connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# instanitate a class for migrations
migrate = Migrate(app=app, db = db)

# we link the app to the db instances
db.init_app(app=app)

# insert cors to allow communication with the client
CORS(app=app)

# since this is a RESTful approach we define our routes for the different resources here

# initialize the api to add resources
api = Api(app=app)

@app.route('/')
def index():

    message = "<h1>Welcome to Veda</h1>"

    return message

# our resources are inserted here

api.add_resource(Categories, "/categories")
api.add_resource(CategoriesById, "/categories/<int:id>")
api.add_resource(Products, "/products")
api.add_resource(ProductById, "/products/<int:id>")
api.add_resource(Reviews, "/reviews")
api.add_resource(ReviewsById, "/reviews/<int:id>")
api.add_resource(Orders, "/orders")
api.add_resource(OrderById, "/orders/<int:id>")
api.add_resource(Items, "/items")
api.add_resource(ItemsById, "/items/<int:id>")
api.add_resource(Register,'/register')
api.add_resource(LogIn,'/sign-in')

if __name__ == "__main__":
    app.run(debug=True)