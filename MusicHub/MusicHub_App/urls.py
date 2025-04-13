from django.urls import path
from . import views
from .views import playlist_detail, add_to_playlist, remove_from_playlist

urlpatterns = [
    path('', views.index, name='home'),
    path('artist/<int:id>/', views.artist_detail, name='artist_detail'),
    path('album/<int:id>/', views.album_detail, name='album_detail'),
    path('track/<int:id>/', views.track_detail, name='track_detail'),
    path('get-lyrics/<int:track_id>/', views.get_track_lyrics, name='get_track_lyrics'),
    path('search/', views.search_artists, name='search'),  
    path('create-artist/', views.create_artist_profile, name='create_artist_profile'),
    path('oauth/callback', views.oauth_callback, name='oauth_callback'),
    path('set-session/', views.set_session_view, name='set_session'),
    path('popular-artists/', views.popular_artists_view, name='popular_artists'),
    path('explore-music/', views.explore_music_view, name='explore_music'),
    path('assistant/', views.ai_assistant, name='ai_assistant'),
    path('playlist/', playlist_detail, name='playlist_detail'),
    path('playlist/add/<int:track_id>/', add_to_playlist, name='add_to_playlist'),
    path('playlist/remove/<int:track_id>/', remove_from_playlist, name='remove_from_playlist'),
]