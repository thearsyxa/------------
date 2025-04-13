from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError  
from .models import Subscription
from MusicHub_App.models import Track
import logging
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")  
            return redirect('profile')
        else:
            messages.error(request, "Ошибка! Неверное имя пользователя или пароль.") 
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Вы успешно вышли из системы.")  
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Регистрация прошла успешно! Теперь вы можете войти.")  
            return redirect('login')
        else:
            messages.error(request, "Ошибка при регистрации. Проверьте введённые данные.")  
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def subscriptions(request):
    return render(request, 'subscriptions.html')


def student_verification(request):
    if request.method == 'POST':
        pass
    return render(request, 'verify_student.html')


def process_payment(request):
    if request.method == 'POST':
        plan = request.POST.get('plan', 'MusicHub Premium')
        price = 10 if plan == 'MusicHub Premium' else 6.5 if plan == 'MusicHub Premium for Students' else 20
        return render(request, 'payment_success.html', {
            'plan': plan,
            'price': price,
        })
    return redirect('subscriptions')


def check_subscription(request, user_id):
    subscription = Subscription.objects.filter(user_id=user_id).first()
    if subscription:
        return JsonResponse({"status": "success", "message" : "Подписка активна"})
    return JsonResponse({"status" : "error", "message" : "Подписка не активна"})
    
    
def download_track(request, user_id, track_name):
    subscription = Subscription.objects.filter(user_id=user_id).first()
    if not subscription:
        return JsonResponse({"status" : "error", "message" : "Нет подписки"})
    track = Track.objects.filter(title=track_name).first()
    if not track:
        return JsonResponse({"status" : "error", "message" : "Трек не найден"})
    return JsonResponse({"status" : "success", "download_url" : track.audio_file.url})
        
        
    


