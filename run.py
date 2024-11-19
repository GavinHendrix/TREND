from app import create_app
from flask import Flask, render_template

if __name__ == '__main__':
    app = create_app(__name__)
    app.run(host='0.0.0.0', port='5050', debug=True)