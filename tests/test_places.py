import pytest
from flask import Flask
from app.src.api.places import places_bp

@pytest.fixture
def app ():
    app = Flask(__name__)
    app.register_blueprint(places_bp, url_prefix='/api')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_nearby_places(client):
    response = client.get('/api/places', query_string= {
                              'location': '40.428263096503805,-86.91173853522032',
                              'radius': '1000',
                              'type': 'restaurant'}
                         )
    assert (response.status_code==200)