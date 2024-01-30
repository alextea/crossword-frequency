# app/__init__.py
from flask import Flask
from app.database.models import db
from app.scripts.get_crosswords import db_cli

app = Flask(__name__)
app.config.from_pyfile('../config.py')

db.init_app(app)  # Initialize Flask-SQLAlchemy
app.cli.add_command(db_cli)

from app import routes
