# Requirements
Python version: >Python 3.8.12
Make sure to have `pip` installed in local enviroment. 
It is recomended to create a new `virtual environment`.

Run `pip install -r requirements.txt` to install dependencies. 

# Authenticate App

## Generate Client ID and Client Secret

1. Register your app following according to (Spotify for developers guidelines)[https://developer.spotify.com/documentation/general/guides/authorization/app-settings/.]
2. Copy '.env-sample' to '.env'
3. Copy the generated 'Cliend ID' and 'Client Secret' in Spotify's dashboard to `SPOTIFY_API_CLIENT_ID` and `SPOTIFY_API_CLIENT_SECRET` in .env. 
4. `SPOTIFY_API_CLIENT_ID` and `SPOTIFY_API_CLIENT_SECRET` will be imported by app and sent as authentication credentials for API calls. 

## Give acces

1. From the app's dashboard (after registration), got to 'users and access'. 
2. Add 

# Run App

While on root directory, run `uvicorn api.fast:app --reload` from CLI to instantiate the server.
2. Go to 


# Target url

- endpoint = http://localhost/api/v1/albums?q=<band-name>  # Endpoint for API
- params = {'q' = band_name}


# Extra Comments

## Album Filter

Returns only albums tagged as "album" by spotify, so no 'singles' or 'compilations' will be returned. 
Can be changed by adjusting parameter `include_groups` in endpoint #'/artist-albums'#