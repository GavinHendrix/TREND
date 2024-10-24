from flask import Flask, render_template
from flask_login import LoginManager
from app.src.db.init import db
from app.src.db.user import User
from app.src.db.survey import Survey
from app.src.config import get_config
from dotenv import load_dotenv

load_dotenv()

def create_app(name):
    app = Flask(name, template_folder='app/templates')
    app.static_folder = 'app/static'

    app.config.from_object(get_config())

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
    from app.src.rec.activities import activities_bp
    from app.src.rec.dining import dining_bp
    from app.src.rec.movies import movies_bp
    from app.src.surv.questions import survey_bp
    from app.src.api.places import places_bp
    from app.src.api.openai import openai_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(errors_bp)
    app.register_blueprint(activities_bp)
    app.register_blueprint(dining_bp)
    app.register_blueprint(movies_bp)
    app.register_blueprint(survey_bp)
    app.register_blueprint(places_bp, url_prefix='/api')
    app.register_blueprint(openai_bp, url_prefix='/api')
    
    return app