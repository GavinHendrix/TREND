from flask import Blueprint, render_template

movies_bp = Blueprint('movies', __name__)

@movies_bp.route('/movies')
def movies():
    return render_template('movies.html')