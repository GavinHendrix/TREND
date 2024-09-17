import requests
from flask import Blueprint, request, jsonify

places_bp = Blueprint('places_bp', __name__)

API_KEY = ""
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
        'key':API_KEY
    }
    response = requests.get(PLACES_URL, params=params)
    data = response.json()

    return jsonify(data)