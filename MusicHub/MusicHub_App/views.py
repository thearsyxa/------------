from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from MusicHub_App.models import Artist, Album, Track
from .utils import get_artist_info, get_wikipedia_summary, summarize_text, get_yandex_music_data

def index(request):
    template = loader.get_template('MusicHub_App/index.html')
    artists = Artist.objects.order_by("-published")
    context = {"artists": artists}
    return HttpResponse(template.render(context, request))

def create_artist_profile(request):
    spotify_artist_id = 'example_id'
    access_token = 'your_access_token'

    artist_info = get_artist_info(spotify_artist_id, access_token)
    artist_name = artist_info['name']
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

    return render(request, 'artist_profile.html', {'artist': artist})


    
    
    
    
    
    
    
    