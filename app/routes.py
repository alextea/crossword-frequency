# app/routes.py
from flask import render_template, url_for
from app import app
from app.database.models import db, Clue, Crossword
from urllib.parse import unquote

@app.route('/')
def index():
    latest_crossword = Crossword.query.order_by(db.desc('date_published')).first()
    clues = Clue.query.filter_by(crossword_id = latest_crossword.id)
    most_common_clues = (
      db.session.query(Clue.solution, db.func.count(Clue.solution).label('count'))
      .group_by(Clue.solution)
      .order_by(db.func.count(Clue.solution).desc())
      .limit(10)
      .all()
    )

    return render_template('index.html', clues=clues, latest_crossword = latest_crossword, most_common_clues = most_common_clues)

@app.route('/solution/<solution>')
def view(solution):
    clue = Clue.query.filter_by(solution=solution).first_or_404()

    clues_and_crosswords = (
        db.session.query(Clue, Crossword)
        .join(Crossword)  # Join with Crossword to get related information
        .filter(Clue.solution == solution)
        .order_by(Crossword.date_published.desc())
        .all()
    )

    return render_template('view.html', clue = clue, clues_and_crosswords = clues_and_crosswords)

@app.route('/crossword/<crossword_id>')
def crossword(crossword_id):
    crossword_id = unquote(crossword_id)
    crossword = Crossword.query.filter_by(id=crossword_id).first_or_404()
    clues = Clue.query.filter_by(crossword_id = crossword_id).all()
    return render_template('crossword.html', crossword=crossword, clues=clues)