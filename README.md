# Requirements
Python version: >Python 3.8.12  
Make sure to have `pip` installed in local enviroment.   
It is recomended to create a new `virtual environment`.

Run `pip install -r requirements.txt` to install dependencies. 

# Authenticate App

## Generate Client ID and Client Secret

1. Register your app following [Spotify for developers guidelines](https://developer.spotify.com/documentation/general/guides/authorization/app-settings/).
2. Copy '.env-sample' to '.env'
3. Copy the generated 'Cliend ID' and 'Client Secret' in Spotify's dashboard to `SPOTIFY_API_CLIENT_ID` and `SPOTIFY_API_CLIENT_SECRET` in .env. 
4. `SPOTIFY_API_CLIENT_ID` and `SPOTIFY_API_CLIENT_SECRET` will be imported by app and sent as authentication credentials for API calls. 

## Give acces

1. From the app's dashboard (after registration), go to 'users and access'. 
2. Give access to desired user for api calls. 

# Run App

While on root directory, run `uvicorn albums_api:app --reload` from CLI to instantiate the server.  
2. Run "http://localhost:8000/api/v1/albums?q=<band-name/>" in web browser, replace `<band-name>` with desired band to search for


# Target url

- endpoint = http://localhost:8000/api/v1/albums?q=<band-name>  # Endpoint for API
- params = {'q' = band_name}


# Extra Comments

## Album Filter

Returns only albums tagged as "album" by spotify, so no 'singles' or 'compilations' will be returned. 
Can be changed by adjusting parameter `include_groups` in endpoint #'/artist-albums'#

## Duplicates

Does not filter duplicates, assuming that every item that spotify stores is unique. 
If duplicates are to be avoided, set `avoid_duplicates` in `get_artist_albums`

## endpoint

- endpoint = `http://localhost:8000/api/v1/albums?q=<band-name>`  # Endpoint for API

Must explicitly set port 8000 when running app 


# Response Status

If no matching artist is found, it will return **404 - No such artist**
If Spotify API is not available, it will return **500 - Internal Server Error**
If Authentication Token expires, it will return **500 - Internal Server**