from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bcrypt import hashpw, checkpw, gensalt
from app.src.db.init import db
from app.src.db.user import User

def create_app(name):
    app = Flask(name, template_folder='app/templates')
    app.static_folder = 'app/static'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SECRET_KEY'] = 'TREND IS THE BEST'

    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return render_template("home.html")
    
    from app.src.auth.login import login_bp
    from app.src.auth.register import register_bp
    from app.src.auth.logout import logout_bp
    from app.src.error import errors_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(errors_bp)

    @app.route('/movies')
    def movies():
        return render_template('movies.html')

    @app.route('/dining')
    def dining():
        return render_template('dining.html')

    @app.route('/activities')
    def activities():
        return render_template('activities.html')
    
    return app