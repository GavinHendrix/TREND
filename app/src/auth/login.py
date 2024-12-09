from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from bcrypt import checkpw
from app.src.db.user import User
# from app.src.db.dining_survey import DiningSurvey
from app.src.db.survey_pref import SurveyPreference

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.query.filter_by(username=username).first()

        if user and checkpw(password, user.password.encode('utf-8')):
            login_user(user)
            flash('Login successful!', 'success')

            if not SurveyPreference.query.filter_by(user_id=user.id).first():
                return redirect(url_for('survey_preference.set_preferences_form'))

            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')