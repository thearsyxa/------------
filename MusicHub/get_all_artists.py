import requests


def get_all_artists(access_token):
    url = "https://api.spotify.com/v1/artists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "limit": 50  
    }

    all_artists = []
    while url:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        all_artists.extend(data['artists']['items'])
        url = data['artists'].get('next')  

    return all_artists

if __name__ == "__main__":
    access_token = 'YOUR_ACCESS_TOKEN'  
    artists = get_all_artists(access_token)
    for artist in artists:
        print(artist)
