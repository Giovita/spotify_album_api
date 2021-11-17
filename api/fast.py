from typing import Optional
import requests
import os
from urllib.parse import urljoin

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests.api import head

from api.auth import get_auth_token

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

@app.get("/")
def index():
    return {"Ok": True}

# Get band_id spotify API


@app.get("/artist") #?q={artist_name}")
def get_artist(artist_name: Optional[str] = None):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    Pick first item returned as default. 
    """
    type = 'artist'
    header = {'Authorization': f'Bearer {auth_token}', 
              'Content-Type': 'application/json'}

    # header = {'Authorization': f'Bearer {auth_token}'}

    # url = urljoin(URI, 'search',  f'?q={artist_name}&type=type')

    url = urljoin(URI, 'search?q=beatles&type=artist')

    print(url)
    
    resp = requests.get(url, headers=header).json()
    
    # print(resp)
    
    artist_id = resp['artists']['items'][0]['id']
    artist_name = resp['artists']['items'][0]['name']
        
    return artist_name, artist_id 
    # return artist_id
    # resp = requests.post(url, data = {q=})

    # print(artist_name)



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