from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField(null = True, blank = True)
    concert_price = models.CharField(max_length= 20, null = True, blank = True)
    published = models.DateTimeField(auto_now_add = True, db_index = True)
    listeners = models.IntegerField(null = True, blank = True)
