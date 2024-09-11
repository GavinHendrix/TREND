from flask import Flask, render_template

def create_app(name):
    app = Flask(name, template_folder='app/templates')
    app.config['SECRET_KEY'] = 'TREND IS THE BEST'
    
    @app.route('/')
    def home_page():
        return render_template("home.html")
    
    @app.route('/base')
    def base_page():
        return render_template("base.html")
    
    return app