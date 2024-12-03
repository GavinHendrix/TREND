from flask import Blueprint, request, jsonify
from app.src.db.dining_survey import DiningSurvey
from app.src.db.init import db

dislike_dining_bp = Blueprint('dislike_dining_bp', __name__)

@dislike_dining_bp.route('/dislike_dining', methods=['POST'])
def dislike_dining():
    # Parse JSON payload
    data = request.json
    user_id = data.get('user_id')
    user_dislike = data.get('user_dislike')

    if not user_id or not user_dislike:
        return jsonify({'error': 'Invalid data. Both user_id and user_dislike are required.'}), 400

    # Query the database for the user survey
    survey_response = DiningSurvey.query.filter_by(user_id=user_id).first()

    if not survey_response:
        return jsonify({'error': 'Survey for the user not found.'}), 404

    # Update the user_dislike column
    survey_response.user_dislike = user_dislike
    db.session.commit()

    return jsonify({'message': f'Dislike for "{user_dislike}" recorded successfully.'}), 200
