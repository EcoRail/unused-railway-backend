# users/urls.py

from django.urls import path
from .views import SignupView, LoginView, ProfileView

urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]