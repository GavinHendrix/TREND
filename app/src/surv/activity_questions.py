from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app.src.db.activity_survey import ActivitySurvey
from app.src.db.init import db
from app.src.rec.preferences import redirect_to_next_survey

activity_survey_bp = Blueprint('activity_survey', __name__)

@activity_survey_bp.route('/activity_survey', methods=['GET', 'POST'])
@login_required
def asurvey():
    if request.method == 'POST':
        responses = ActivitySurvey(
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
        )
        db.session.add(responses)
        db.session.commit()

        flash('Survey submitted successfully!', 'success')
        # return redirect(url_for('home'))
        return redirect_to_next_survey()

    return render_template('activity_survey.html')