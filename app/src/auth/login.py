from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from bcrypt import checkpw
from app.src.db.user import User

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = User.query.filter_by(username=username).first()

        if user and checkpw(password, user.password.encode('utf-8')):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')