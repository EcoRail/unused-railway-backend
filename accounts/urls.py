from django.urls import path
from .views import RegisterView, UserView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # POST /api/auth/register/ : 회원가입
    path('register/', RegisterView.as_view(), name='register'),
    
    # POST /api/auth/login/ : 로그인 (Access, Refresh 토큰 발급)
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # POST /api/auth/login/refresh/ : Access 토큰 재발급
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # GET, PUT, DELETE /api/auth/user/ : 프로필 조회, 수정, 탈퇴
    path('user/', UserView.as_view(), name='user_view'),
    
    # POST /api/auth/logout/ : 로그아웃 (Refresh 토큰 비활성화)
    path('logout/', LogoutView.as_view(), name='logout'),
]
