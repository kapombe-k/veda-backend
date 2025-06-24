from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS

from models import db


# we initiate the flask app
app = Flask(__name__)

# let's connect the database using the connection string
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# instanitate a class for migrations
migrate = Migrate(app=app, db = db)

# we link the app to the db instances
db.init_app(app=app)

# since this is a RESTful approach we define our routes for the different resources here

# initialize the api to add resources
api = Api(app=app)