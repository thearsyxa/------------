from django.urls import path
from MusicHub_App.views import index, create_artist_profile, artist_profile, album_detail, oauth_callback, set_session_view


urlpatterns = [
    path('', index, name='home'),
    path('create-artist/', create_artist_profile, name= 'create_artist_profile'),
    path('artist/<int:artist_id>/', artist_profile, name='artist_profile'),
    path('album/<int:album_id>/', album_detail, name='album_detail'),
    path('oauth/callback', oauth_callback, name='oauth_callback'),
    path('set-session/', set_session_view, name='set_session'),
]