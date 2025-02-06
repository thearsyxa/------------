import requests
from django.core.management.base import BaseCommand
from MusicHub_App.models import Artist
from MusicHub_App.utils import get_artist_info, get_wikipedia_summary, summarize_text, get_yandex_music_data

class Command(BaseCommand):
    help = 'Импорт данных из Spotify и Википедии'

    def handle(self, *args, **kwargs):
        spotify_artist_id = 'example_id'
        access_token = 'your_access_token'

        artist_info = get_artist_info(spotify_artist_id, access_token)
        artist_name = artist_info['name']
        wikipedia_summary = get_wikipedia_summary(artist_name)
        
        if wikipedia_summary:
            artist_description = summarize_text(wikipedia_summary)
        else:
            artist_description = "Описание не найдено."

        yandex_music_listeners = get_yandex_music_data('track_id', 'yandex_access_token')

        artist, created = Artist.objects.get_or_create(
            name=artist_name,
            defaults={'description': artist_description, 'listeners': yandex_music_listeners}
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f'Добавлен новый исполнитель: {artist_name}'))
        else:
            self.stdout.write(self.style.WARNING(f'Исполнитель {artist_name} уже существует'))
