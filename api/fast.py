from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv
from requests.api import head
import base64
from pprint import pprint



URI = 'https://api.spotify.com/v1'

# Load app auth credentials from .env.
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')


# Setup Client
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Allows all origins
    allow_credentials = True,
    allow_methods = ["*"],  # Allow al lmethods
    allow_headers = ["*"],  # Allow all headers
)
# headers = {'header': ''}

## Request authorization.
AUTH_URL = 'https://accounts.spotify.com/api/token'
# print('CLIENT_ID :', CLIENT_ID)
# print('CLIENT SECRET: ', CLIENT_SECRET)

auth_str = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode('ascii')).decode('ascii')

# print(auth_str)

auth_header = {'Authorization': f'Basic {auth_str}',
               'Content-Type': 'application/x-www-form-urlencoded'}
auth_body = {'grant_type': 'client_credentials'}

auth_resp = requests.post(AUTH_URL,headers=auth_header, data=auth_body).json()

pprint(auth_resp)

token = auth_resp.get('access_token', auth_resp.get('error'))

# print(token)


@app.get("/")
def index():
    return {"Ok": True}

# Get band_id spotify API

@app.get("/tracks_testAPI")
def get_tracks():
    url = 'https://api.spotify.com/v1/tracks/2TpxZ7JUBn3uw46aR7qd6V'
    header = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=header)
    return r.json()

@app.get("/artist")
def get_artist(artist_name):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    Pick first item returned as default. 
    """


    
    type = 'artist'

    print(artist_name)