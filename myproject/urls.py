# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from users.views import LoginView # LoginView를 제대로 임포트하는지 확인하세요.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/login/', LoginView.as_view(), name='login'), # 당신의 커스텀 로그인 URL입니다.
]