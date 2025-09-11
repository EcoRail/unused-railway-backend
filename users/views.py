# users/views.py
from rest_framework import status, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Proposal


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import UserSerializer, LoginSerializer, ProfileSerializer, ProposalSerializer
from .models import Proposal
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "유효하지 않은 아이디 또는 비밀번호입니다."}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProposalViewSet(viewsets.ModelViewSet):
    """
    제안(Proposal) CRUD 및 추천 API
    - 목록/생성: /api/proposals/
    - 상세/수정/삭제: /api/proposals/{id}/
    - 추천하기/취소: /api/proposals/{id}/recommend/
    """
    queryset = Proposal.objects.all().order_by('-created_at')
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 제안 생성 시 작성자를 현재 로그인한 사용자로 자동 설정
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def recommend(self, request, pk=None):
        proposal = self.get_object()
        user = request.user
        
        # 이미 추천했다면 취소, 아니면 추가 (토글 방식)
        if user in proposal.recommended_by.all():
            proposal.recommended_by.remove(user)
            return Response({'status': 'recommendation removed'}, status=status.HTTP_200_OK)
        else:
            proposal.recommended_by.add(user)
            return Response({'status': 'recommendation added'}, status=status.HTTP_200_OK)