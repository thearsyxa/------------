import requests
from transformers import pipeline

def search_artists(query, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "q": query,
        "type": "artist",
        "limit": 50  # Максимальное количество записей за один запрос
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json().get('artists', {}).get('items', [])

def get_artist_info(spotify_artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{spotify_artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json()

def get_albums_info(spotify_artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{spotify_artist_id}/albums"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    return response.json().get('items', [])

def get_tracks_info(album_id, access_token):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            return response.json().get('items', [])
        except ValueError:
            return []
    else:
        print(f"Ошибка при получении треков для альбома {album_id}: {response.status_code}")
        return []

def get_wikipedia_summary(artist_name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{artist_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("extract")
    return None

# Явно указываем модель для summarization
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_text(text):
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    return summary[0]['summary_text']

def get_yandex_music_data(track_id, access_token):
    url = f"https://api.music.yandex.net/v1/tracks/{track_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        track_data = response.json()
        return track_data.get("play_count")
    return None
