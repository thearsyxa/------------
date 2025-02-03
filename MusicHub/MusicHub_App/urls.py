from django.urls import path
from MusicHub_App.views import index

urlpatterns = [
    path('', index)
]