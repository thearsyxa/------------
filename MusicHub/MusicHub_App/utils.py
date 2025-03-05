import requests
from transformers import pipeline
from .spotify import get_spotify_token
import time
import json
import os

CACHE_FILE = 'cache.json'
REQUEST_LIMIT = 5  # Лимит запросов за определенное время
REQUEST_INTERVAL = 60  # Интервал времени в секундах

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=4)

cache = load_cache()
request_timestamps = []

def manage_request_limit():
    current_time = time.time()
    request_timestamps.append(current_time)
    while len(request_timestamps) > REQUEST_LIMIT:
        first_request = request_timestamps.pop(0)
        if current_time - first_request < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - (current_time - first_request))

def get_artist_info(spotify_artist_id, access_token):
    if spotify_artist_id in cache:
        return cache[spotify_artist_id]
    
    manage_request_limit()
    url = f"https://api.spotify.com/v1/artists/{spotify_artist_id}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        cache[spotify_artist_id] = response.json()
        save_cache(cache)
        return cache[spotify_artist_id]
    
    return None

def get_albums_info(spotify_artist_id, access_token):
    cache_key = f"{spotify_artist_id}_albums"
    if cache_key in cache:
        return cache[cache_key]
    
    manage_request_limit()
    url = f"https://api.spotify.com/v1/artists/{spotify_artist_id}/albums"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        cache[cache_key] = response.json()['items']
        save_cache(cache)
        return cache[cache_key]
    
    return None

def get_tracks_info(album_id, access_token):
    cache_key = f"{album_id}_tracks"
    if cache_key in cache:
        return cache[cache_key]
    
    manage_request_limit()
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        cache[cache_key] = response.json()['items']
        save_cache(cache)
        return cache[cache_key]
    
    return None

def get_spotify_track_info(track_title):
    manage_request_limit()
    url = f"https://api.spotify.com/v1/search?q={track_title}&type=track&limit=1"
    headers = {
        "Authorization": f"Bearer {get_spotify_token()}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 401:  # Token expired, refresh token and retry
        access_token = get_spotify_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        track_data = response.json()['tracks']['items']
        if track_data:
            return track_data[0]
    elif response.status_code == 429:
        time.sleep(5)  # Задержка в 5 секунд перед повторным запросом
        return get_spotify_track_info(track_title)
    else:
        raise Exception(f"Failed to get track info for {track_title}. Status code: {response.status_code}")
    
    return None

def get_wikipedia_summary(artist_name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{artist_name}"
    response = requests.get(url)
    return response.json().get("extract") if response.status_code == 200 else None

summarizer = pipeline("summarization")

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
