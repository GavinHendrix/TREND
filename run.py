from app import create_app
from flask import Flask, render_template
import os

if __name__ == '__main__':
    app = create_app(__name__)
    port = int(os.getenv("PORT", 5050))
    app.run(host="0.0.0.0", port=port, debug=False)
