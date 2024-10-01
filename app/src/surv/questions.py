from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, login_required
from bcrypt import checkpw
from app.src.db.user import User
from flask import Blueprint, render_template
from app.src.db.survey import Survey
from app.src.db.init import db

survey_bp = Blueprint('survey', __name__)

@survey_bp.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    if request.method == 'POST':
        # Collect responses from the form
        responses = Survey(
            user_id=current_user.id,
            question1=request.form['question1'],
            question2=request.form['question2'],
            question3=request.form['question3'],
            # question4=request.form['question4'],
            # question5=request.form['question5'],
            # question6=request.form['question6'],
            # question7=request.form['question7'],
            # question8=request.form['question8'],
            # question9=request.form['question9'],
            # question10=request.form['question10'],
        )
        db.session.add(responses)
        db.session.commit()

        flash('Survey submitted successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('survey.html')