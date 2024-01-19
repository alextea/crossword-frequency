# database/models.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Crossword(Base):
    __tablename__ = 'crosswords'

    id = Column(String, primary_key=True)
    web_title = Column(String)
    web_url = Column(String)
    date_published = Column(DateTime)

    clues = relationship('Clue', back_populates='crossword')

    def __repr__(self):
        return f"<Crossword(id={self.id}, web_title={self.web_title}, web_url={self.web_url}, date_published={self.date_published})>"

class Clue(Base):
    __tablename__ = 'clues'

    id = Column(Integer, primary_key=True)
    crossword_id = Column(String, ForeignKey('crosswords.id'))
    clue_number = Column(Integer)
    clue_direction = Column(String)
    clue_text = Column(String)
    solution = Column(String)

    crossword = relationship('Crossword', back_populates='clues')

    def __repr__(self):
        return f"<Clue(id={self.id}, crossword_id={self.crossword_id}, clue_number={self.clue_number}, clue_direction={self.clue_direction}, clue_text={self.clue_text}, solution={self.solution})>"
