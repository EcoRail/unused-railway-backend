from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # 인증된 사용자만 쓰기 가능

    def perform_create(self, serializer):
        serializer.save(author=self.request.user) # 현재 로그인된 사용자를 작성자로 저장