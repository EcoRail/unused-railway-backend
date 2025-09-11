# users/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, LoginSerializer, ProfileSerializer

class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    # 🚨 아래 두 줄을 추가하세요.
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # 1. 아이디와 비밀번호로 사용자 인증 시도
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            # 2. 인증 성공 시, 사용자에게 토큰 발급 (없으면 새로 생성)
            token, created = Token.objects.get_or_create(user=user)
            
            # 3. 토큰과 함께 사용자 정보를 응답으로 반환
            return Response({
                "token": token.key,
                "username": user.username,
                "email": user.email,
            }, status=status.HTTP_200_OK)
        
        # 4. 인증 실패 시
        return Response({"error": "유효하지 않은 아이디 또는 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)