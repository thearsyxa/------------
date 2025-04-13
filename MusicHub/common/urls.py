from django.urls import path
from .views import login_view, logout_view, profile_view, register_view, subscriptions, student_verification, process_payment, check_subscription, download_track

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('register/', register_view, name='register'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    path('verify-student/', student_verification, name='student_verification'),
    path('process-payment/', process_payment, name='process_payment'),
    path('api/check-subscription/<int:user_id>/', check_subscription),
    path('api/download-track/<int:user_id>/<str:track_name>/', download_track),
]
