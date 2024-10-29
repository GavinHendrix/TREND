import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash
from app.src.db.dining_survey import DiningSurvey

dining_places_bp = Blueprint('dining_places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@dining_places_bp.route('/dining_places', methods=['GET'])
def get_nearby_places():
    user_id = int(request.args.get('user_id'))
    location = request.args.get('location')  # Format: 'lat,lng'
    place_type = request.args.get('type') # 'restaurant'

    survey_response = DiningSurvey.query.filter_by(user_id=user_id).first()
    if not survey_response:
        flash('Survey Error', 'danger')

    keywords = []
    if survey_response.question1:
        keywords.append(survey_response.question1)

    radius_m = 5000 # default value (5m)
    if survey_response.question2:
        radius_km = int(survey_response.question2)
        radius_m = radius_km * 1000
    
    if survey_response.question3 and survey_response.question3 != "No Restrictions":
        keywords.append(survey_response.question3)

    if survey_response.question4 and int(survey_response.question4) >= 7:
        keywords.append('ambient')
    
    price_mapping = {
        "Budget ($)": (0, 1),
        "Moderate ($$)": (1, 2),
        "Expensive ($$$)": (2, 3),
        "Luxury ($$$$)": (3, 4)
    }
    minprice, maxprice = price_mapping.get(survey_response.question5, (0, 4))

    if survey_response.question6:
        keywords.append(survey_response.question6)

    if survey_response.question7 and survey_response.question7 != "No Preference":
        keywords.append(survey_response.question7)
    
    # question 8?

    if survey_response.question8 and int(survey_response.question8) >= 7:
        keywords.append('sustainable')
        keywords.append('locally-sourced')

    keyword_query = ' '.join(keywords)

    params = {
        'location': location,
        'radius': radius_m,
        'type': place_type,
        'key': GOOGLE_API_KEY,
        'keyword': keyword_query,
        'minprice': minprice,
        'maxprice': maxprice,
        'opening_hours': {'open_now': True}
    }

    response = requests.get(PLACES_URL, params=params)
    data = response.json()

    if data['status'] == 'ZERO_RESULTS':
        return jsonify({'error': 'No places found near your location'}), 404

    return jsonify(data)

# call only works if API key is .env
# Post call filters(Cannot be a param)
#'price_level': 0/1/2/3/4  //0:free, 1:Inexpensive, 2:Moderate, 3:Expensive, 4:Very Expensive