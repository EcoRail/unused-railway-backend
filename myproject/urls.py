# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from users.views import LoginView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/login/', LoginView.as_view(), name='login')
]