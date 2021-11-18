from fastapi import testclient
from fastapi.testclient import TestClient
from urllib.parse import urljoin

from albums_api import app
import utils.tester_app as tester_app

client_app = TestClient(app)

url = '/api/v1/albums'

def test_no_artist():
    response = client_app.get(url)
    assert response.status_code == 422  # Value Missing
    
def test_artist_ok():
    url_query = urljoin(url, '?q=beatles')
    response = client_app.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == list
    assert not response.json() == False
    
def test_artist_ok():
    url_query = urljoin(url, '?q=not_really_a_band')
    response = client_app.get(url_query)
    assert response.status_code == 404  # Custom response_status_not found
    

client_testUtils = TestClient(tester_app.app)

def test_get_artist():
    url_query = urljoin(url, '/artists?q=not_really_a_band')
    response = client_testUtils.get(url_query)
    assert response.status_code == 404
    assert response.json() == r'404 - No such artist'
    
def test_artist_ok():
    url_query = urljoin(url, '/artists?q=beatles')
    response = client_testUtils.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == str
    assert not response.json() == False
    
def test_get_albums():
    artist = '3WrFJ7ztbogyGnTHbHJFl2'  # Beatles
    url_query = urljoin(url, f'/albums?artist={artist}')
    response = client_testUtils.get(url_query)
    assert response.status_code == 200
    assert type(response.json()) == list
    assert type(response.json()[0]) == dict
    assert not response.json() == False
    assert set(response.json()[0].keys()) == {'name', 'released', 'tracks', 'cover'}

def test_duplicates():
    artist = '3WrFJ7ztbogyGnTHbHJFl2'  # Beatles
    url_query_duplicates = urljoin(url, f'/albums?artist={artist}')
    url_query_no_duplicates = urljoin(url, f'/albums-no-duplicate?artist={artist}')
    response_duplicates = client_testUtils.get(url_query_duplicates)
    response_no_duplicates = client_testUtils.get(url_query_no_duplicates)

    assert response_no_duplicates.status_code == 200
    assert len(response_duplicates.json()) == len(response_no_duplicates.json())
    
    albums_duplicate = [album['name'] for album in response_duplicates.json()]
    albums_no_duplicate = [album['name'] for album in response_no_duplicates.json()]
    
    assert len(set(albums_duplicate)) == len(albums_no_duplicate)
    
    
# TODO : verify if wrong auth token is passed?