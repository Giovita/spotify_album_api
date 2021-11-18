import albums_api
from fastapi import FastAPI, Response, status

app = albums_api.app

@app.get('/artists', status_code=200)
def get_artist(q, response:Response):
    return albums_api.get_artist(q, response)

@app.get('/albums', status_code=200)
def get_artist_albums(artist, response: Response, avoid_duplicates=False):
    return albums_api.get_artist_albums(artist, response)

@app.get('/albums-no-duplicate', status_code=200)
def get_artist_albums_no_duplicates(artist, response: Response, avoid_duplicates=True):
    return albums_api.get_artist_albums(artist, response, avoid_duplicates)
