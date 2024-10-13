from openai import OpenAI
import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Blueprint, request, jsonify

openai_bp = Blueprint('openai_bp', __name__)

# Get Path for .env File and Load
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
#OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  replaced by below line 
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'),) # does not actually need the param as that is the default param

def get_recommendation(messages, model="gpt-3.5-turbo", max_tokens=50, temperature=.7):
    recommendation = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return recommendation

@openai_bp.route('/get-recommendation', methods=['POST'])
def recommendation_route():
    data = request.json
    prompt = data.get('prompt')
    messages = [{"role": "user", "content": prompt}]
    model = data.get('model', "gpt-3.5-turbo")
    max_tokens = data.get('max_tokens', 100)      # optional input with 100 default
    temperature = data.get('temperature', .7)     # optional input with .7 default
    # temperature is creativity level?

    recommendation = get_recommendation(messages=messages, model=model, max_tokens=max_tokens, temperature=temperature)
    return jsonify({'recommendation' : recommendation})