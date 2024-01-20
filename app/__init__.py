# app/__init__.py
from flask import Flask
from app.database.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../crossword_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from app.database.database_operations import init_db

db.init_app(app)  # Initialize Flask-SQLAlchemy

from app import routes
