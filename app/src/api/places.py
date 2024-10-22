import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify

places_bp = Blueprint('places_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

PLACES_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

@places_bp.route('/places', methods=['GET'])

def get_nearby_places() :
    location = request.args.get('location')  # Format: 'lat,lng'
    radius = request.args.get('radius')  # In meters
    place_type = request.args.get('type') # 'restaurant'

    params = {
        'location':location,
        'radius':radius,
        'type':place_type,
        'key':GOOGLE_API_KEY,
        'opening_hours': {'open_now': True}
        #,'price_level': 0/1/2/3/4  //0:free, 1:Inexpensive, 2:Moderate, 3:Expensive, 4:Very Expensive
    }
    response = requests.get(PLACES_URL, params=params)
    data = response.json()

    return jsonify(data)

# call only works if API key is .env