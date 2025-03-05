import requests
from django.conf import settings

def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_data = {
        'grant_type': 'client_credentials',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    response = requests.post(auth_url, data=auth_data)
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception("Failed to obtain Spotify token. Status code: {}".format(response.status_code))
