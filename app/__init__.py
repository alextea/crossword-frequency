# app/__init__.py
from flask import Flask
from app.database.models import db
from app.scripts.get_crosswords import db_cli

app = Flask(__name__)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_pre_ping': True}  # recover from database restarts
app.config.from_pyfile('../config.py', silent=True)
app.config.from_prefixed_env()  # e.g. FLASK_SQLALCHEMY_DATABASE_URI, FLASK_GUARDIAN_API_KEY

db.init_app(app)  # Initialize Flask-SQLAlchemy
app.cli.add_command(db_cli)

from app import routes
