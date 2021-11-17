from typing import Optional
import requests
import os
from urllib.parse import urljoin

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests.api import head

from api.auth import get_auth_token

# from auth import get_auth_token

from pprint import pprint

URI = 'https://api.spotify.com/v1/'

# Request authorization through Client Credentials workflow 
# https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/

load_dotenv()
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

auth_token = get_auth_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET)   

# Setup Client
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Allows all origins
    allow_credentials = True,
    allow_methods = ["*"],  # Allow al lmethods
    allow_headers = ["*"],  # Allow all headers
)

header = {'Authorization': f'Bearer {auth_token}', 
          'Content-Type': 'application/json'}


@app.get("/artist") #?q={artist_name}")
# @app.get("/artist?q={artist_name}")
def get_artist(q):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. 
    https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    Pick first item returned as default. 
    """

    artist_url = urljoin(URI, f'search?q={q}&type=artist')

    print(artist_url)
    
    resp = requests.get(artist_url, headers=header).json()
    
    artist_id = resp['artists']['items'][0]['id']
    artist_name = resp['artists']['items'][0]['name']
        
    return artist_name, artist_id 
    
@app.get('/artist-albums')
def get_artist_albums(artist, avoid_duplicates=False):
    """
    From artist ID, return a list of every album of the artist from Spotify's API
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-albums
    """
        
    url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset=0')  # Filters only "album" types
    resp = requests.get(url, headers=header).json()

    avoid_duplicates = True  # Uncomment to prevent duplicates in output. 

    albums = []
    page = 0
    while resp.get('items'):
        url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset={page}')   
        resp = requests.get(url, headers=header).json()
        
        for album in resp.get('items'):
            name = album['name']
            if not avoid_duplicates or not name in albums:
                albums.append(name)
            
        page += 50
    
    return albums
    
def get_artist_albums(artist, avoid_duplicates=False):
    """
    From artist ID, return a list of every album of the artist from Spotify's API
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-albums
    """
        
    url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset=0')  # Filters only "album" types
    resp = requests.get(url, headers=header).json()

    avoid_duplicates = True  # Uncomment to prevent duplicates in output. 

    albums = []
    page = 0
    while resp.get('items'):
        url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset={page}')   
        resp = requests.get(url, headers=header).json()
        
        for album in resp.get('items'):
            name = album['name']
            if not avoid_duplicates or not name in albums:
                albums.append(name)
            
        page += 50
    
    return albums

print(get_artist_albums('0k17h0D3J5VfsdmQ1iZtE9'))

# http://localhost:8000/api/v1/albums?q=<band-name>  # Endpoint for API

@app.get('/api/v1/albums')
def get_albums(q):
    pass
    


#############################
@app.get("/")
def index():
    return {"Ok": True}

# Test endpoint for auth workflow
@app.get("/tracks_testAPI")
def get_tracks():
    url = 'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V'
    header = {'Authorization': f'Bearer {auth_token}'}
    r = requests.get(url, headers=header)
    return r.json()


# Test endpoint for auth workflow
@app.get("/test_searchAPI")
def test_search():
    url = 'https://api.spotify.com/v1/search?q=beatles&type=track' 
    header = {'Authorization': f'Bearer {auth_token}'}
    r = requests.get(url, headers=header)
    return r.json()