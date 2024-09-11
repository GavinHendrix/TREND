from app import create_app
from flask import Flask, render_template

app = create_app(__name__)

@app.route('/login')
def login():
    return render_template('auth/login.html')

if __name__ == '__main__':
    app.run(debug=True)