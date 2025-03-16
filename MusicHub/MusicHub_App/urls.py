from django.urls import path
from MusicHub_App.views import index, create_artist_profile, artist_profile, album_detail, oauth_callback, set_session_view, popular_artists_view, explore_music_view
from . import views

urlpatterns = [
    path('', index, name='home'),
    path('artist/<int:id>/', views.artist_detail, name='artist_detail'),
    path('album/<int:id>/', views.album_detail, name='album_detail'),
    path('track/<int:id>/', views.track_detail, name='track_detail'),
    path('search/', views.search_artists, name='search_artists'),
    path('create-artist/', create_artist_profile, name= 'create_artist_profile'),
    path('oauth/callback', oauth_callback, name='oauth_callback'),
    path('set-session/', set_session_view, name='set_session'),
    path('popular-artists/', popular_artists_view, name='popular_artists'),
    path('explore-music/', explore_music_view, name='explore_music'),

]