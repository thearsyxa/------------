from django.contrib import admin
from .models import Artist, Album, Track

try:
    admin.site.unregister(Artist)
except admin.sites.NotRegistered:
    pass


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'concert_price', 'listeners', 'avatar', 'genre')  
    search_fields= ('name', )
    

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'avatar')
    search_fields = ('title', 'artist__name')
    

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_artist_name', 'album', 'duration')
    list_filter = ('album', 'artist')
    search_fields = ('title', 'artist__name', 'album__title')
    autocomplete_fields = ('album',)
   

    def get_artist_name(self, obj):
        return obj.artist.name if obj.artist else 'Исполнитель не указан'
    get_artist_name.short_description = 'Исполнитель'

