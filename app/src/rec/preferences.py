from flask import Blueprint, flash, request, redirect, url_for, render_template, session
from app.src.db.init import db
from app.src.db.survey_pref import SurveyPreference
from flask_login import current_user

survey_preference_bp = Blueprint('survey_preference', __name__)

@survey_preference_bp.route('/set_preferences', methods=['POST'])
def set_preferences():
    preferences = SurveyPreference.query.filter_by(user_id=current_user.id).first()
    if not preferences:
        preferences = SurveyPreference(user_id=current_user.id)
    
    preferences.dining_survey = 'dining' in request.form.getlist('surveys')
    preferences.activity_survey = 'activity' in request.form.getlist('surveys')
    preferences.movie_survey = 'movie' in request.form.getlist('surveys')

    db.session.add(preferences)
    db.session.commit()
    
    session['remaining_surveys'] = []
    if preferences.dining_survey:
        session['remaining_surveys'].append('dining')
    if preferences.activity_survey:
        session['remaining_surveys'].append('activity')
    if preferences.movie_survey:
        session['remaining_surveys'].append('movie')

    return redirect_to_next_survey()


def redirect_to_next_survey():
    if 'remaining_surveys' in session and session['remaining_surveys']:
        next_survey = session['remaining_surveys'].pop(0)
        session.modified = True
        
        if next_survey == 'dining':
            return redirect(url_for('dining_survey.dsurvey'))
        elif next_survey == 'activity':
            return redirect(url_for('activity_survey.asurvey'))
        elif next_survey == 'movie':
            return redirect(url_for('movie_survey.msurvey'))
    
    return redirect(url_for('home'))

@survey_preference_bp.route('/set_preferences_form', methods=['GET'])
def set_preferences_form():
    return render_template('preference.html')