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


def get_artist(q):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. 
    https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    Pick first item returned as default. 
    """

    artist_url = urljoin(URI, f'search?q={q}&type=artist')

    resp = requests.get(artist_url, headers=header).json()
    
    artist_id = resp['artists']['items'][0]['id']
    artist_name = resp['artists']['items'][0]['name']
        
<<<<<<< HEAD:albums_api.py
    # return artist_name, artist_id 
    return artist_id
=======
    return artist_name, artist_id 
>>>>>>> 983aabc748cd6f42c8f0162be2791b4e112ef537:api/fast.py
    
def get_artist_albums(artist, avoid_duplicates=False):
    """
    From artist ID, return a list of every album of the artist from Spotify's API
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-albums
    """
<<<<<<< HEAD:albums_api.py
        
    url = urljoin(URI, f'artists/{artist}/albums?include_groups=album&limit=49&offset=0')  # Filters only "album" types
    resp = requests.get(url, headers=header).json()

    # avoid_duplicates = True  # Uncomment to prevent duplicates in output. 

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

# http://localhost:8000/api/v1/albums?q=<band-name>  # Endpoint for API

@app.get('/api/v1/albums')
def get_albums(q):
    """
    Gets a list of all albums from artist 'q' from Spotify API. 
    """
    artist_id = get_artist(q)
=======
    
    # artist = "3WrFJ7ztbogyGnTHbHJFl2"  # The Beatles
    artist = "0k17h0D3J5VfsdmQ1iZtE9"  # Pink Floyd
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
>>>>>>> 983aabc748cd6f42c8f0162be2791b4e112ef537:api/fast.py
    
    artist_albums = get_artist_albums(artist_id, avoid_duplicates=True)
    
    return artist_albums
