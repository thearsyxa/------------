from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from MusicHub_App.models import Artist, Album, Track, Playlist, PlaylistTrack
from .utils import get_artist_info, get_wikipedia_summary, summarize_text, get_yandex_music_data
from .forms import SearchForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .text_generation import generate_text
from .wikipedia_search import search_wikipedia


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
 

def artist_detail(request, id):
    artist = get_object_or_404(Artist, id=id)
    albums = artist.album_set.all()
    tracks = Track.objects.filter(album__artist=artist)
    return render(request, 'artist_detail.html', {'artist': artist, 'albums': albums, 'tracks': tracks})


def album_detail(request, id):  
    album = get_object_or_404(Album, id=id)
    tracks = album.track_set.all()
    return render(request, 'album_detail.html', {'album': album, 'tracks': tracks})

def track_detail(request, id):
    track = get_object_or_404(Track, id=id)
    album = track.album
    artist = album.artist
    return render(request, 'track_detail.html', {'track': track, 'album': album, 'artist': artist})


def search_artists(request):
    form = SearchForm()
    artist_results = []
    album_results = []
    track_results = []
    query = ''
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query'].lower()
            artist_results = [artist for artist in Artist.objects.all() if query in artist.name.lower()]
            album_results = [album for album in Album.objects.all() if query in album.title.lower()]
            track_results = [track for track in Track.objects.all() if query in track.title.lower()]
            
    return render(request, 'search.html', {
        'form': form,
        'artist_results': artist_results,
        'album_results': album_results,
        'track_results': track_results,
        'query': query
    })
    
    
def index_view(request):
    popular_artists = Artist.objects.order_by('-popularity')[:5] 
    recommended_tracks = []  
    is_auth = request.user.is_authenticated
    return render(request, 'index.html', {
        'popular_artists': popular_artists,
        'recommended_tracks': recommended_tracks,
        'is_auth': is_auth
    })
    
    
def popular_artists_view(request):
    artists = Artist.objects.order_by('-listeners')[:10]  
    return render(request, 'popular_artists.html', {'artists': artists})


def explore_music_view(request):
    return render(request, 'explore_music.html')


def get_track_lyrics(request, track_id):
    try:
        track = Track.objects.get(id=track_id)
        if track.lyrics:
            return JsonResponse({'lyrics': track.lyrics})
        else:
            return JsonResponse({'error': 'Текст песни отсутствует.'}, status=404)
    except Track.DoesNotExist:
        return JsonResponse({'error': 'Трек не найден.'}, status=404)
    

def ai_assistant(request):
    return HttpResponse("Hello, this is the AI Assistant page!")

    
@login_required
def add_to_playlist(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    playlist, _ = Playlist.objects.get_or_create(user=request.user)
    PlaylistTrack.objects.create(playlist=playlist, track=track)
    existing_track = PlaylistTrack.objects.filter(playlist=playlist,track=track).exists()
    if not existing_track:
        PlaylistTrack.objects.create(playlist=playlist, track=track)
        messages.success(request, f"Трек '{track.title}' добавлен в плейлист!")
    else:
        messages.info(request, f"Трек '{track.title}' уже есть в вашем плейлисте.")
    return redirect('playlist_detail')


@login_required
def playlist_detail(request):
    playlist = Playlist.objects.filter(user=request.user).first()
    return render(request, 'playlist_detail.html', {'playlist':playlist})


@login_required
def remove_from_playlist(request, track_id):
    playlist = Playlist.objects.filter(user=request.user).first()
    if not playlist:
        return JsonResponse({'success': False, 'message': 'Плейлист не найден'})

    track = PlaylistTrack.objects.filter(playlist=playlist, track_id=track_id).first()
    if track:
        track.delete()
        return JsonResponse({'success': True, 'message': 'Трек успешно удален'})
    return JsonResponse({'success': False, 'message': 'Трек не найден'})


