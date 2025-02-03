from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from MusicHub_App.models import Artist

def index(request):
    template = loader.get_template('MusicHub_App/index.html')
    artists = Artist.objects.order_by("-published")
    context = {"artists": artists}
    return HttpResponse(template.render(context, request))
    
    
    
    
    
    
    
    
    # query = Artist.objects.all()
    # responce = "" 
    # for artist in query:
    #     responce+=f"{artist.name}\n"  
    # return HttpResponse(responce)
