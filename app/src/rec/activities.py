from flask import Blueprint, render_template

activities_bp = Blueprint('activities', __name__)

@activities_bp.route('/activities')
def activities():
    return render_template('activities.html')