import os
import urllib.parse

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crossword_database.db'
    PORT = 8000

class ProductionConfig(Config):
    DEBUG = False
    database_name = os.environ.get('DATABASE_NAME')
    database_user = os.environ.get('DATABASE_USER')
    database_pass = urllib.parse.quote(os.environ.get('DATABASE_PASSWORD'))
    database_host = 'localhost'
    
    SQLALCHEMY_DATABASE_URI = f"postgresql://{database_user}:{database_pass}@{database_host}/{database_name}"
    PORT = os.environ.get('PORT', 5000)

# Determine the environment based on an environment variable
env = os.environ.get('FLASK_ENV', 'development')
app_config = DevelopmentConfig if env == 'development' else ProductionConfig
