from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.src.db.dining_survey import DiningSurvey
from app.src.db.init import db

dining_survey_bp = Blueprint('dining_survey', __name__)

@dining_survey_bp.route('/dining_survey', methods=['GET', 'POST'])
@login_required
def dsurvey():
    if request.method == 'POST':
        responses = DiningSurvey(
            user_id=current_user.id,
            question1=request.form['question1'],
            question2=request.form['question2'],
            question3=request.form['question3'],
            question4=request.form['question4'],
            question5=request.form['question5'],
            question6=request.form['question6'],
            question7=request.form['question7'],
            question8=request.form['question8'],
            question9=request.form['question9'],
            question10=request.form['question10'],
        )
        db.session.add(responses)
        db.session.commit()

        flash('Survey submitted successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('dining_survey.html')