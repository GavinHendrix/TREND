import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash
from app.src.db.activity_survey import ActivitySurvey

activities_places_bp = Blueprint('activities_places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@activities_places_bp.route('/activities_places', methods=['GET'])
def get_nearby_places():
    if request.args.get('user_id') == '':
        return jsonify({'error': 'It looks like you don\'t have an account yet. Please create one to continue!'}), 404
    
    user_id = int(request.args.get('user_id'))
    location = request.args.get('location')  # Format: 'lat,lng'
    type = "art_gallery"  #night_club art_gallery bowling_alley

    survey_response = ActivitySurvey.query.filter_by(user_id=user_id).first()
    if not survey_response:
        flash('Survey Error', 'danger')

    keywords = []
    activity_types = survey_response.question1.split(',')

    radius_m = 5000 # default value (5m)
    if survey_response.question2:
        radius_km = int(survey_response.question2)
        radius_m = radius_km * 1000
    
    # budget = survey_response.question3
    # time_of_day = survey_response.question4
    # indoor_outdoor = survey_response.question5
    # group_size = survey_response.question8
    # specific_preferences = survey_response.question9
    # rating_or_popularity = survey_response.question10
    
    # if survey_response.question3 and survey_response.question3 != "No Restrictions":
    #     keywords.append(survey_response.question3)

    params = {
        'location': location,
        'radius': radius_m,
        'type': 'point_of_interest',
        'key': GOOGLE_API_KEY,
        #'keyword': keyword_query,
        #'minprice': minprice,
        #'maxprice': maxprice,
        'opening_hours': {'open_now': True}
    }
    response = requests.get(PLACES_URL, params=params)
    data = response.json()

    if data['status'] == 'ZERO_RESULTS':
        return jsonify({'error': 'No places found near your location'}), 404

    return jsonify(data)