# database/database_operations.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()

def record_exists(session, Model, record_id):
    # Query the database to check if a record with the given ID exists
    existing_record = session.query(Model).filter_by(id=record_id).first()

    # If existing_record is not None, a record with the given ID exists
    return existing_record is not None