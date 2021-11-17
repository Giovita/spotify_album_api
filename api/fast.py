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
# @app.get("/artist?q={artist_name}")
def get_artist(q):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. 
    https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    Pick first item returned as default. 
    """
    # type = 'artist'
    header = {'Authorization': f'Bearer {auth_token}', 
              'Content-Type': 'application/json'}

    artist_url = urljoin(URI, f'search?q={q}&type=artist')

    print(artist_url)
    
    resp = requests.get(artist_url, headers=header).json()
    
    artist_id = resp['artists']['items'][0]['id']
    artist_name = resp['artists']['items'][0]['name']
        
    return artist_name, artist_id 
    
@app.get('/artist-albums')
def get_artist_albums(artist):
    """
    From artist ID, return a list of every album of the artist from Spotify's API
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-albums
    """
    
    # artist = "3WrFJ7ztbogyGnTHbHJFl2"  # The Beatles
    # artist = "0k17h0D3J5VfsdmQ1iZtE9"  # Pink Floyd
    header = {'Authorization': f'Bearer {auth_token}', 
              'Content-Type': 'application/json'}
    # url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&offset=10')  # Filters only "album" types

    # resp = requests.get(url, headers=header).json()

    # albums = []
    # for album in resp.get('items'):
    #     albums.append(album['name'])

    # # return albums
    # if resp.get('items'):
    #     is_empty = False
    # elif not resp.get('items'):
    #     is_empty = True
        
    page = 0
    albums = []
    url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset=0')  # Filters only "album" types

    resp = requests.get(url, headers=header).json()
    while resp.get('items'):
        url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset={page}')   
        # url = urljoin(URI, f'artists/{artist}/albums?&limit=49&offset={page}')   
        resp = requests.get(url, headers=header).json()
        for album in resp.get('items'):
            albums.append(album['name'])

        page += 50
    
    # url = urljoin(URI, f'artists/{artist}/albums?limit=10')  # Filters only "album" types
    # resp = requests.get(url, headers=header).json()
    # for album in resp.get('items'):
    #     albums.append(album['name'])
    
    
    print(len(albums))
    
    next = resp['next']
    return albums
    
    # artist_url = urljoin(URI, f'search?q={q}&type=artist')
    
    pass

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