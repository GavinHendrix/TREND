import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash

activities_places_bp = Blueprint('activities_places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@activities_places_bp.route('/places', methods=['GET'])
def get_nearby_places():
    user_id = int(request.args.get('user_id'))
    location = request.args.get('location')  # Format: 'lat,lng'
    params = {
        'location': location,
        'radius': 500,
        'type': "bowling",
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