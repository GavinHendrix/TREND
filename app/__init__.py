from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
from bcrypt import hashpw, checkpw, gensalt

def create_app(name):
    app = Flask(name, template_folder='app/templates')
    app.static_folder = 'app/static'
    app.config['SECRET_KEY'] = 'TREND IS THE BEST'

    # app = Flask(__name__)
    # app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db = SQLAlchemy(app)
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    class User(db.Model, UserMixin):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(150), nullable=False, unique=True)
        password = db.Column(db.String(150), nullable=False)

    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return render_template("home.html")
    
    @app.route('/login', methods=['GET', 'POST'])
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
    
    @app.route('/register', methods=['GET', 'POST'])
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

    from app.src.auth.logout import auth_bp as logout_bp
    app.register_blueprint(logout_bp, url_prefix='/auth')
    
    # @app.route('/logout')
    # @login_required
    # def logout():
    #     logout_user()
    #     return redirect(url_for('home'))

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