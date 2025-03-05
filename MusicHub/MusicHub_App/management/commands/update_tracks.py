from django.core.management.base import BaseCommand
from MusicHub_App.models import Track
from MusicHub_App.utils import get_spotify_track_info

class Command(BaseCommand):
    help = 'Обновление данных треков и добавление spotify_id'

    def handle(self, *args, **kwargs):
        tracks = Track.objects.filter(is_updated=False)  

        for track in tracks:
            try:
                spotify_track_info = get_spotify_track_info(track.title)
                if spotify_track_info:
                    track.spotify_id = spotify_track_info['id']
                    track.is_updated = True  
                    track.save()
                    self.stdout.write(self.style.SUCCESS(f'Обновлен трек: {track.title}'))
                else:
                    self.stdout.write(self.style.ERROR(f'Не удалось найти данные для трека: {track.title}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при обновлении трека {track.title}: {e}"))


