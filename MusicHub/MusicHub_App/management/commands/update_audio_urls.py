import spotipy
from spotipy.oauth2 import SpotifyOAuth
from django.core.management.base import BaseCommand
from MusicHub_App.models import Track
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelень)s - %(message)s')
logger = logging.getLogger(__name__)

# Настройка Spotify API
SPOTIPY_CLIENT_ID = 'cddafd384a6b410186c5590513258e54'
SPOTIPY_CLIENT_SECRET = '67c0e5b8758d4971aded0856298ed853'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8000/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope="user-library-read"))

def get_spotify_track_url(track_title):
    results = sp.search(q=track_title, type='track', limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        return track['external_urls']['spotify']
    else:
        logger.warning(f"Не удалось найти трек на Spotify: {track_title}")
        return None

class Command(BaseCommand):
    help = 'Обновление URL аудиофайлов для треков'

    def handle(self, *args, **kwargs):
        tracks = Track.objects.all()
        for track in tracks:
            if not track.audio_url:
                audio_url = get_spotify_track_url(track.title)
                if audio_url:
                    track.audio_url = audio_url
                    track.save()
                    self.stdout.write(self.style.SUCCESS(f'Обновлен URL аудиофайла для трека: {track.title}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Не удалось найти аудиофайл для трека: {track.title}'))
