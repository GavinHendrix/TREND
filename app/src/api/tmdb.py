from platform import release
import requests
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify, flash
from app.src.db.movie_survey import MovieSurvey
from app.src.db.survey_pref import SurveyPreference

tmdb_bp = Blueprint('tmdb_bp', __name__)

env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

TMDB_BASE_URL = 'https://api.themoviedb.org/3'

@tmdb_bp.route('/tmdb', methods=['GET'])
def get_movies_by_criteria():
    if request.args.get('user_id') == '':
        return jsonify({'error': 'It looks like you don\'t have an account yet. Please create one to continue!'}), 404

    user_id = int(request.args.get('user_id'))

    survey_pref = SurveyPreference.query.filter_by(user_id=user_id).first()
    if not survey_pref.movie_survey:
        return jsonify({'error': 'This survey has not been completed.'}), 404

    survey_response = MovieSurvey.query.filter_by(user_id=user_id).first()

    url = f"{TMDB_BASE_URL}/discover/movie"
    headers = {'accept': 'application/json'}
    params = {
        'api_key': TMDB_API_KEY,
        # 'langauge': survey_response.question1,
        'language': 'en-US',
        # 'with_genres': '28',
        'with_genres': survey_response.question2,
        'without_genres': survey_response.question3,
        'release_date.gte': survey_response.question4,
        # 'release_date.gte': '2020-01-01',
        'include_adult': 'false'
          #include genres 28 - action, 35 - comedy //multiple genres can be included by using a comma
        # could add 'without_genres': , 'release_date.gte': , 'include_adult': , 'with_runtime.lte': 
    }

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code != 200:
        return jsonify({'error': 'Failed request to tmdb'})
    
    data = response.json()
    return jsonify(data)