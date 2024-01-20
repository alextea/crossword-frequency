from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Crossword(db.Model):
    __tablename__ = 'crosswords'

    id = db.Column(db.String, primary_key=True)
    web_title = db.Column(db.String)
    web_url = db.Column(db.String)
    date_published = db.Column(db.DateTime)

    clues = db.relationship('Clue', back_populates='crossword')

    def __repr__(self):
        return f"<Crossword(id={self.id}, web_title={self.web_title}, web_url={self.web_url}, date_published={self.date_published})>"

class Clue(db.Model):
    __tablename__ = 'clues'

    id = db.Column(db.Integer, primary_key=True)
    crossword_id = db.Column(db.String, db.ForeignKey('crosswords.id'))
    clue_number = db.Column(db.Integer)
    clue_direction = db.Column(db.String)
    clue_text = db.Column(db.String)
    solution = db.Column(db.String)

    crossword = db.relationship('Crossword', back_populates='clues')

    def __repr__(self):
        return f"<Clue(id={self.id}, crossword_id={self.crossword_id}, clue_number={self.clue_number}, clue_direction={self.clue_direction}, clue_text={self.clue_text}, solution={self.solution})>"
