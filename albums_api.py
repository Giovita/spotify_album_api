import requests
import os
from urllib.parse import urljoin

from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware

from utils.auth import get_auth_token

spotify_api_base_URI = 'https://api.spotify.com/v1/'

# Load app auth credentials from .env.
load_dotenv()
AUTH_URL = 'https://accounts.spotify.com/api/token'
CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

auth_response, auth_token = get_auth_token(AUTH_URL, CLIENT_ID, CLIENT_SECRET) 

# Setup Client
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],  # Allows all origins
    allow_credentials = True,
    allow_methods = ["*"],  # Allow all methods
    allow_headers = ["*"],  # Allow all headers
)

header = {'Authorization': f'Bearer {auth_token}', 
          'Content-Type': 'application/json'}

def get_artist(q, response:Response):

    """ 
    Use '/search' api endpoint to find 'artist_id' for a given name. 
    https://developer.spotify.com/documentation/web-api/reference/#/operations/search    Pick first item returned as default. 
    """

    artist_url = urljoin(spotify_api_base_URI, f'search?q={q}&type=artist')

    resp = requests.get(artist_url, headers=header).json()
    
    artists_found = resp.get('artists', )['items']
    
    if not artists_found:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "404 - No such artist"
    
    artist_id = artists_found[0]['id']
    return artist_id
    
    
def get_artist_albums(artist, response: Response, avoid_duplicates=False):
    """
    From artist ID, return a list of every album of the artist from Spotify's API
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-an-artists-albums
    """
        
    url = urljoin(spotify_api_base_URI, 
                  f'artists/{artist}/albums?include_groups=album&limit=50&offset=0')  # Filters only "album" types
    resp = requests.get(url, headers=header).json()

    albums = []
    albums_name = []
    
    while url:
        for album in resp.get('items'):
            album_dict = {'name': album['name'],
                            'released': album['release_date'],
                            'tracks': album['total_tracks'],
                            'cover': {'height': album.get('images', 'No Cover Image')[0]['height'],
                                    'width': album.get('images', 'No Cover Image')[0]['width'],
                                    'url': album.get('images', 'No Cover Image')[0]['url'],
                                    } 
                                }

            if not avoid_duplicates or not album_dict['name'] in albums_name:
                albums_name.append(album_dict['name'])
                albums.append(album_dict)
                
        url = resp.get('next')
        if url:
            resp = requests.get(url, headers=header).json()
    return albums


@app.get('/api/v1/albums', status_code=200)
def get_albums(q, response:Response):
    """
    Gets a list of all albums from artist 'q' from Spotify API. 
    """
    artist_id = get_artist(q, response)
    
    if response.status_code == 404:
        return artist_id
    
    # Pass False to avoid_duplicates=True to prevent repetition
    artist_albums = get_artist_albums(artist_id, response, )
    return artist_albums
