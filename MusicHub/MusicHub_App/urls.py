from django.urls import path
from MusicHub_App.views import index
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('create-artist/', views.create_artist_profile, name = 'create_artist_profile')
]