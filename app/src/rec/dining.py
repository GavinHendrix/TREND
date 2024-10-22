from flask import Blueprint, render_template

dining_bp = Blueprint('dining', __name__)

@dining_bp.route('/dining')
def dining():
    return render_template('dining.html')