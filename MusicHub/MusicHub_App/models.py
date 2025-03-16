from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length = 100)
    bio = models.TextField()
    description = models.TextField(null = True, blank = True)
    concert_price = models.CharField(max_length= 20, null = True, blank = True)
    published = models.DateTimeField(auto_now_add = True, db_index = True)
    listeners = models.IntegerField(null = True, blank = True)
    
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
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Альбомы"
        verbose_name = "Альбом"
        ordering = ('-release_date',)
        
        
class Track(models.Model):
    album = models.ForeignKey(Album, on_delete= models.CASCADE)
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
    
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "Треки"
        verbose_name = "Трек"
        ordering = ('-title',)
        

        
              
        
