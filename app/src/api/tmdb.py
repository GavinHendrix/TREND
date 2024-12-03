from platform import release
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash

tmdb_bp = Blueprint('tmdb_bp', __name__)

env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@tmdb_bp.route('/tmdb', methods=['GET'])
def get_movies_by_criteria():
    url = f"{TMDB_BASE_URL}/discover/movie"
    headers = {'accept': 'application/json'}
    params = {
        'api_key': TMDB_API_KEY,
        'language': 'en-US',
        'with_genres': '28',
        'include_adult': 'false',
        'release_date.gte': '2020-01-01'
          #include genres 28 - action, 35 - comedy //multiple genres can be included by using a comma
        # could add 'without_genres': , 'release_date.gte': , 'include_adult': , 'with_runtime.lte': 
    }

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed request to tmdb'})
    
    data = response.json()
    return jsonify(data)