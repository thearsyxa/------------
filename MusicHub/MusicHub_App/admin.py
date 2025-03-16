from django.contrib import admin
from .models import Artist, Album, Track

try:
    admin.site.unregister(Artist)
except admin.sites.NotRegistered:
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'concert_price', 'listeners')  # Обновите поля для отображения

admin.site.register(Album)
admin.site.register(Track)
