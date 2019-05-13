import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

login_manager = LoginManager()

app = Flask(__name__)

app.config["SECRET_KEY"] = "mysecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/trailfinderflask'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

CORS(app)

login_manager.init_app(app)
login_manager.login_view = "login"
