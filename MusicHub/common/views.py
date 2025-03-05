from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    form = AuthenticationForm()  
    return render(request, 'registration/login.html', {'form': form})


def some_view(request):
    is_auth = request.user.is_authenticated  
    return render(request, 'template_name.html', {'is_auth': is_auth})


def logout_view(request):
    return render(request, 'registration/logout.html')

def profile_view(request):
    return render(request, 'profile.html')

def register_view(request):
    return render(request, 'registration/register.html')