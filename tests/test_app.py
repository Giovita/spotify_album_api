from fastapi.testclient import TestClient

from albums_api import app

from urllib.parse import urljoin

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