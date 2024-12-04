from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.src.db.movie_survey import MovieSurvey
from app.src.db.init import db
from app.src.rec.preferences import redirect_to_next_survey

movie_survey_bp = Blueprint('movie_survey', __name__)

@movie_survey_bp.route('/movie_survey', methods=['GET', 'POST'])
@login_required
def msurvey():
    if request.method == 'POST':
        question2=request.form.getlist('question2[]')
        question3=request.form.getlist('question3[]')

        responses = MovieSurvey(
            user_id=current_user.id,
            question1=request.form['question1'],
            question2='|'.join(question2),
            question3='|'.join(question3),
            question4=request.form['question4'],
        )
        db.session.add(responses)
        db.session.commit()

        flash('Survey submitted successfully!', 'success')
        # return redirect(url_for('home'))
        return redirect_to_next_survey()

    return render_template('movie_survey.html')