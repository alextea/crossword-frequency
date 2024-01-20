# app/routes.py
from flask import render_template, request, redirect, url_for
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

    total_clues = Clue.query.count()
    total_across = Clue.query.filter_by(clue_direction = 'across').count()
    total_down = Clue.query.filter_by(clue_direction = 'down').count()
    total_crosswords = Crossword.query.count()

    return render_template('index.html',
                           clues=clues,
                           latest_crossword = latest_crossword,
                           most_common_clues = most_common_clues,
                           total_clues = total_clues,
                           total_across = total_across,
                           total_down = total_down,
                           total_crosswords = total_crosswords
                           )

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

    across_count = Clue.query.filter_by(solution=solution, clue_direction='across').count()
    down_count = Clue.query.filter_by(solution=solution, clue_direction='down').count()

    return render_template('view.html', 
                           clue = clue,
                           clues_and_crosswords = clues_and_crosswords,
                           across_count = across_count,
                           down_count = down_count
                           )

@app.route('/crossword/<crossword_id>')
def crossword(crossword_id):
    crossword_id = unquote(crossword_id)
    crossword = Crossword.query.filter_by(id=crossword_id).first_or_404()
    clues = Clue.query.filter_by(crossword_id = crossword_id).all()
    return render_template('crossword.html', crossword=crossword, clues=clues)

@app.route('/find-word', methods=['POST'])
def find_word():
    word = request.form.get('solution')
    word = process_string(word)

    print(f"search: {word}")

    return redirect(url_for('view', solution=word))


def process_string(input_string):
    # Use list comprehension to filter out non-alphabetic characters
    # and then join the characters to form a new string
    cleaned_string = ''.join(char.upper() for char in input_string if char.isalpha())
    return cleaned_string