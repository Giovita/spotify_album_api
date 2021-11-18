import requests
import os
from dotenv import load_dotenv
import base64

# Load app auth credentials from .env.
load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

AUTH_URL = 'https://accounts.spotify.com/api/token'

def get_auth_token(url, client_id, client_secret):
    """
    Request authorization through Client Credentials workflow 
    https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/
    """

    auth_str = base64.b64encode(f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')

    auth_header = {'Authorization': f'Basic {auth_str}',
                'Content-Type': 'application/x-www-form-urlencoded'}
    auth_body = {'grant_type': 'client_credentials'}
    auth_resp = requests.post(url,headers=auth_header, data=auth_body)
    
    
    auth_token = auth_resp.json().get('access_token', auth_resp.json().get('error'))
    
    return auth_resp.status_code, auth_token

