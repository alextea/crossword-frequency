# app/__init__.py
from flask import Flask
from config import app_config
from app.database.models import db

app = Flask(__name__)
app.config.from_object(app_config)

from app.database.database_operations import init_db

db.init_app(app)  # Initialize Flask-SQLAlchemy

from app import routes
