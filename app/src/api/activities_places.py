import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash
from app.src.db.activity_survey import ActivitySurvey
from app.src.db.survey_pref import SurveyPreference

activities_places_bp = Blueprint('activities_places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

ACTIVITY_MAPPING = {
    "Arts and Culture": {"keywords": ["art_gallery", "museum", "art", "culture", "historical sites"]},
    "Outdoor and Nature": {"keywords": ["park", "nature", "hiking", "gardens"]},
    "Music and Entertainment": {"keywords": ["movie_theatre", "night_club", "live music", "concerts"]},
    "Shopping": {"keywords": ["shopping_mall", "store", "retail", "boutiques", "markets"]},
    "Fitness and Sports": {"keywords": ["gym", "stadium", "fitness", "sports center", "yoga"]},
    "Animal Encounters": {"keywords": ["zoo", "pet store", "wildlife", "aquarium"]},
    "Games and Challenges": {"keywords": ["amusement_park", "escape_room", "arcade", "gaming"]},
    "Adventure and Thrills": {"keywords": ["amusement_park", "roller coaster", "extreme sports"]},
    "Quiet Spaces": {"keywords": ["library", "park", "meditation", "relaxation"]}
}

@activities_places_bp.route('/activities_places', methods=['GET'])
def get_nearby_places():
    if request.args.get('user_id') == '':
        return jsonify({'error': 'It looks like you don\'t have an account yet. Please create one to continue!'}), 404
    
    user_id = int(request.args.get('user_id'))
    location = request.args.get('location')  # Format: 'lat,lng'

    survey_pref = SurveyPreference.query.filter_by(user_id=user_id).first()
    if not survey_pref.activity_survey:
        return jsonify({'error': 'This survey has not been completed.'}), 404

    survey_response = ActivitySurvey.query.filter_by(user_id=user_id).first()

    radius_m = 5000 # default value (5m)
    if survey_response.question2:
        radius_km = int(survey_response.question2)
        radius_m = radius_km * 1000

    price_mapping = {
        "Low": (0, 1),
        "Medium": (1, 2),
        "High": (2, 3)
    }
    minprice, maxprice = price_mapping.get(survey_response.question3, (0, 3))

    keywords = []

    if survey_response.question4 and survey_response.question4 != "Anytime":
        keywords.append(survey_response.question4)

    if survey_response.question5 and survey_response.question5 != "Both":
        keywords.append(survey_response.question5)

    if survey_response.question6 and survey_response.question6 != "No":
        keywords.append("family-friendly")

    if survey_response.question7:
        keywords.append(survey_response.question7)

    if survey_response.question8 and survey_response.question8 != "None":
        keywords.append(survey_response.question8)
    
    if survey_response.question9 and survey_response.question9 != "None":
        keywords.append(survey_response.question9)

    activity = survey_response.question1
    activity_details = ACTIVITY_MAPPING.get(activity.strip())
    
    # Query using 'keywords'
    combined_keywords = activity_details["keywords"] + keywords
    combined_keyword_query = ' '.join(combined_keywords)
    params = {
        'location': location,
        'radius': radius_m,
        'key': GOOGLE_API_KEY,
        'keyword': combined_keyword_query,
        'minprice': minprice,
        'maxprice': maxprice,
        'opening_hours': {'open_now': True}
    }
    response = requests.get(PLACES_URL, params=params)
    data = response.json()
    
    if data['status'] == 'ZERO_RESULTS':
        return jsonify({'error': 'No places found near your location'}), 404

    # return jsonify(data)
    return jsonify({'results': data.get('results', [])})