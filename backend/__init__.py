import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/trailfinderflask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db = SQLAlchemy(app)
Migrate(app, db)

CORS(app)

# login_manager.init_app(app)
# login_manager.login_view = "login"
