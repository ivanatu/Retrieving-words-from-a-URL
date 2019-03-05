import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import psycopg2

url_app = Flask(__name__)
url_app.config.from_object(Config)
url_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# url_app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
db = SQLAlchemy(url_app)
db.init_app(url_app)
# migrate = Migrate(app, db)

from app import views, models

