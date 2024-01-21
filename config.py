import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///crossword_database.db'
    PORT = 8000

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'
    PORT = os.environ.get('PORT', 5000)

# Determine the environment based on an environment variable
env = os.environ.get('FLASK_ENV', 'development')
app_config = DevelopmentConfig if env == 'development' else ProductionConfig
