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

@tmdb_bp.route('/tmdb/movies', methods=['GET'])
def get_movies_by_criteria():
    params = {
        'api_key': TMDB_API_KEY,
        'langauage': 'en-US',
        'with_genres': '28' #include genres 28 - action, 35 - comedy //multiple genres can be included by using a comma
        # could add 'without_genres': , 'release_date.gte': , 'include_adult': , 'with_runtime.lte': 
    }

    response = requests.get(f"{TMDB_BASE_URL}/discover/movie", params=params)
    data = response.json()
    
    return jsonify(data)