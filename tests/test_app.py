from dotenv.main import load_dotenv
from fastapi.testclient import TestClient
from albums_api import app, get_artist_albums
from urllib.parse import urljoin
from dotenv import load_dotenv
from utils.auth import get_auth_token
import os


client = TestClient(app)

url = '/api/v1/albums'

def test_no_artist():
    response = client.get(url)
    assert response.status_code == 422  # Value Missing
    
def test_artist_ok():
    url_query = urljoin(url, '?q=beatles')
    response = client.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == list
    assert not response.json() == False
    
def test_artist_ok():
    url_query = urljoin(url, '?q=not_really_a_band')
    response = client.get(url_query)
    assert response.status_code == 404  # Custom response_status_not found
    
    
# TODO : verify if wrong auth token is passed?


URI = 'https://api.spotify.com/v1/'

load_dotenv()
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

auth_response, auth_token = get_auth_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)   

def test_get_artist():
    url_query = urljoin(url, '/artists?q=not_really_a_band')
    response = client.get(url_query)
    assert response.status_code == 404
    assert response.json() == r'404 - No such artist'
    
def test_artist_ok():
    url_query = urljoin(url, '/artists?q=beatles')
    response = client.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == str
    assert not response.json() == False
    
def test_get_albums():
    artist = '3WrFJ7ztbogyGnTHbHJFl2'  # Beatles
    url_query = urljoin(url, f'/albums?artist={artist}')
    response = client.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == list
    assert not response.json() == False
    assert set(response.json()[0].keys()) == {'name', 'released', 'tracks', 'cover'}

# def test_duplicates():
    