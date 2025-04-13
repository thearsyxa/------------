from django.db import models
from PIL import Image
from django.contrib.auth.models import User


class Artist(models.Model):
    name = models.CharField(max_length = 100)
    bio = models.TextField()
    description = models.TextField(null = True, blank = True)
    concert_price = models.CharField(max_length= 20, null = True, blank = True)
    published = models.DateTimeField(auto_now_add = True, db_index = True)
    listeners = models.IntegerField(null = True, blank = True)
    avatar = models.ImageField(upload_to='artist_avatars/', null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.avatar:
            img = Image.open(self.avatar.path)
            max_size = (400, 400)
            img.thumbnail(max_size)  
            img.save(self.avatar.path)  
    
    def __str__(self):
        return self.name+ " "+str(self.concert_price)
    
    class Meta:
        verbose_name_plural = "Исполнители"
        verbose_name = "Исполнитель"
        ordering = ('-published',)
        
class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='album_avatars/', null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.avatar:
            img = Image.open(self.avatar.path)
            max_size = (450, 450)
            img.thumbnail(max_size)
            img.save(self.avatar.path)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Альбомы"
        verbose_name = "Альбом"
        ordering = ('-release_date',)
        
        
class Track(models.Model):
    album = models.ForeignKey(Album, on_delete= models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length = 100)
    duration = models.DurationField()
    play_count = models.IntegerField(null = True, blank=True)
    audio_file = models.FileField(upload_to='tracks/', default='tracks/default.mp3')  
    description = models.TextField(default='No description')
    release_date = models.DateField(default='2000-01-01')
    genre = models.CharField(max_length=50, default='Unknown')
    spotify_id = models.CharField(max_length=50, null=True, blank=True)
    is_updated = models.BooleanField(default=False)
    audio_url = models.URLField(max_length=1024, null=True, blank=True)
    audio_file = models.FileField(upload_to='tracks/')
    lyrics = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Треки"
        verbose_name = "Трек"
        ordering = ('-title',)
        


class Playlist(models.Model):
    name = models.CharField(max_length=100, default="Любимые треки")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks')
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
        

        
              
        
