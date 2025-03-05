import requests
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from MusicHub_App.models import Artist, Album, Track
from MusicHub_App.utils import search_artists, get_artist_info, get_albums_info, get_tracks_info, get_wikipedia_summary, summarize_text, get_yandex_music_data
from MusicHub_App.spotify import get_spotify_token

class Command(BaseCommand):
    help = 'Импорт данных из Spotify и Википедии'

    def handle(self, *args, **kwargs):
        access_token = get_spotify_token()
        specific_artists = ["Джизус", "Три дня дождя", "Nirvana", "System of a Down", "Юлия Савичева", "Metallica", "Ваня Дмитриенко", "Michael Bublé", "PHARAOH", "Нервы"]

        for artist_name in specific_artists:
            try:
                self.stdout.write(self.style.SUCCESS(f"Поиск исполнителя: {artist_name}"))
                
                artists = search_artists(artist_name, access_token)
                if not artists:
                    self.stdout.write(self.style.ERROR(f"Не удалось найти исполнителя: {artist_name}"))
                    continue

                for artist_data in artists:
                    try:
                        spotify_artist_id = artist_data['id']
                        self.stdout.write(self.style.SUCCESS(f"Найден исполнитель: {artist_data['name']} (ID: {spotify_artist_id})"))
                        artist_info = get_artist_info(spotify_artist_id, access_token)
                        self.stdout.write(self.style.SUCCESS(f"Ответ API: {artist_info}"))

                        if 'name' in artist_info:
                            artist_name = artist_info['name']
                        else:
                            self.stdout.write(self.style.ERROR(f"Ключ 'name' отсутствует в ответе API для артиста с ID {spotify_artist_id}."))
                            continue

                        wikipedia_summary = get_wikipedia_summary(artist_name)

                        if wikipedia_summary:
                            artist_description = summarize_text(wikipedia_summary)
                        else:
                            artist_description = "Описание не найдено."

                        artist, created = Artist.objects.get_or_create(
                            name=artist_name,
                            defaults={'description': artist_description}
                        )

                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Добавлен новый исполнитель: {artist_name}'))
                        else:
                            self.stdout.write(self.style.WARNING(f'Исполнитель {artist_name} уже существует'))

                        albums_info = get_albums_info(spotify_artist_id, access_token)
                        if not albums_info:
                            self.stdout.write(self.style.ERROR(f"Не удалось получить альбомы для исполнителя: {artist_name}"))
                        for album_info in albums_info:
                            release_date = album_info.get('release_date', '0001-01-01')
                            try:
                                release_date = datetime.strptime(release_date, '%Y-%m-%d').date()
                            except ValueError:
                                try:
                                    release_date = datetime.strptime(release_date, '%Y').date()
                                    release_date = release_date.replace(month=1, day=1)
                                except ValueError:
                                    release_date = datetime(1, 1, 1).date()

                            album, created = Album.objects.get_or_create(
                                artist=artist,
                                title=album_info['name'],
                                release_date=release_date,
                                defaults={'genre': ', '.join(album_info.get('genres', []))}
                            )
                            if created:
                                self.stdout.write(self.style.SUCCESS(f'Добавлен новый альбом: {album.title}'))

                            tracks_info = get_tracks_info(album_info['id'], access_token)
                            if not tracks_info:
                                self.stdout.write(self.style.ERROR(f"Не удалось получить треки для альбома: {album_info['name']}"))
                            for track_info in tracks_info:
                                Track.objects.get_or_create(
                                    album=album,
                                    title=track_info['name'],
                                    duration=timedelta(milliseconds=track_info['duration_ms']), 
                                    defaults={'play_count': track_info.get('play_count'), 'spotify_id': track_info.get('id')}
                                )
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"Ошибка при импорте данных для артиста: {e}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при выполнении поиска: {e}"))

