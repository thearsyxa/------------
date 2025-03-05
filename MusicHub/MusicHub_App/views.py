from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from MusicHub_App.models import Artist, Album, Track
from .utils import get_artist_info, get_wikipedia_summary, summarize_text, get_yandex_music_data
from .spotify import get_spotify_token


def index(request):
    template = loader.get_template('MusicHub_App/index.html')
    artists = Artist.objects.order_by("-published")
    messages.add_message(request, messages.SUCCESS, "Confirm!")
    context = {"artists": artists}
    return HttpResponse(template.render(context, request))


def create_artist_profile(request):
    spotify_artist_id = '0TnOYISbd1XYRBk9myaseg'
    access_token = 'BQD8aXlX0hfpV-Ljl1_r7guIUDelV0D9305rm5i-ky6CGZFH7jPPCwKbU2lwhbUcWniYad57S9lgIdyUrB6yO5PbTKEN90DdxydYz9xe0207n1KhD6dd8Jps1lxZ-wv87fkVQ0Vju-U'

    artist_info = get_artist_info(spotify_artist_id, access_token)
    artist_name = artist_info.get('name', 'Unknown Artist')
        
    wikipedia_summary = get_wikipedia_summary(artist_name)
    
    if wikipedia_summary:
        artist_description = summarize_text(wikipedia_summary)
    else:
        artist_description = "Описание не найдено."

    yandex_music_listeners = get_yandex_music_data('track_id', 'yandex_access_token')

    artist = Artist.objects.create(
        name=artist_name,
        description=artist_description,
        listeners=yandex_music_listeners
    )

    return render(request, 'MusicHub_App/artist_profile.html', {'artist': artist})


def artist_profile(request, artist_id):
    artist = get_object_or_404(Artist, pk=artist_id)
    albums = artist.album_set.all()
    return render(request, 'MusicHub_App/artist_profile.html', {'artist': artist, 'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'MusicHub_App/album_detail.html', {'album':album})


def oauth_callback(request):
    messages.add_message(request, messages.SUCCESS, "OAuth авторизация успешна!")
    return redirect('home')


def example_view(request):
    response = render(request, 'artist_profile.html')
    if not request.COOKIES.get("user_data"):
        response.set_cookie(
            "user_data", 
            "Some user-specific data",
            max_age=3600,
            httponly=True,
            secure=False,
            samesite="None"
            )
    return response

def set_session_view(request):
    request.session['user_name'] = 'Some user-specific data'  
    return HttpResponse("Done!")

  
    
    





    
    
    
    
    
    
    
    