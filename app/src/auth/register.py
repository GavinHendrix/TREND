from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user
from bcrypt import hashpw, gensalt
from app.src.db.user import User
from app.src.db.init import db

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hashed_password = hashpw(password, gensalt(12))
        new_user = User(username=username, password=hashed_password.decode('utf-8'))
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.')
        return redirect(url_for('login'))
    return render_template('register.html')