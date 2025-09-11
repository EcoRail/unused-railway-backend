# users/urls.py

from django.urls import path
from .views import SignupView, LoginView, ProfileView, ProposalViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('proposals', ProposalViewSet, basename='proposal')


urlpatterns = [
    path('register/', SignupView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls))
]