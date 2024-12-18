import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash
from app.src.db.dining_survey import DiningSurvey
from app.src.db.survey_pref import SurveyPreference
import random

dining_places_bp = Blueprint('dining_places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@dining_places_bp.route('/dining_places', methods=['GET'])
def get_nearby_places():
    if request.args.get('user_id') == '':
        return jsonify({'error': 'It looks like you don\'t have an account yet. Please create one to continue!'}), 404

    user_id = int(request.args.get('user_id'))
    location = request.args.get('location')  # Format: 'lat,lng'
    place_type = request.args.get('type') # 'restaurant'

    survey_pref = SurveyPreference.query.filter_by(user_id=user_id).first()
    if not survey_pref.dining_survey:
        return jsonify({'error': 'This survey has not been completed.'}), 404

    survey_response = DiningSurvey.query.filter_by(user_id=user_id).first()

    # Get disliked restaurant names
    disliked_places = survey_response.user_dislike.split(',') if survey_response.user_dislike else []

    cuisine_options = ["American", "Italian", "Mexican", "Indian", "Chinese", "Mediterranean", "Japanese"]
    keywords = []
    if survey_response.question1 and survey_response.question1 != "Other":
        keywords.append(survey_response.question1)
        cuisine_options.remove(survey_response.question1)

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

    if survey_response.question8 and int(survey_response.question8) >= 7:
        keywords.append(random.choice(cuisine_options))

    if survey_response.question9 and survey_response.question9 != "No Preference":
        keywords.append(survey_response.question9)

    if survey_response.question10 and int(survey_response.question10) >= 7:
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

    # Filter out disliked places
    filtered_results = [
        place for place in data.get('results', [])
        if place.get('name') not in disliked_places
    ]

    if not filtered_results:
        return jsonify({'error': 'No places found after filtering dislikes.'}), 404

    filtered_with_photos = []
    for place in filtered_results:
        if 'photos' in place and len(place['photos']) > 0:
            photo_reference = place['photos'][0]['photo_reference']
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=300&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
        else:
            photo_url = 'https://via.placeholder.com/300x150'

        place['photo_url'] = photo_url
        filtered_with_photos.append(place)

    # return jsonify({'results': filtered_results})
    return jsonify({'results': filtered_with_photos})

# call only works if API key is .env
# Post call filters(Cannot be a param)
#'price_level': 0/1/2/3/4  //0:free, 1:Inexpensive, 2:Moderate, 3:Expensive, 4:Very Expensive