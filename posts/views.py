from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostListDetailSerializer, PostCreateUpdateSerializer, CommentSerializer


class PostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Post.objects.all().order_by('-created_at')
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateUpdateSerializer
        return PostListDetailSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        railway_property_id = self.request.query_params.get('railway_property')
        if railway_property_id:
            queryset = queryset.filter(railway_property_id=railway_property_id)
        return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['get'], url_path='my_posts')
    def my_posts(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='recommended_posts')
    def recommended_posts(self, request):
        posts = Post.objects.filter(recommendations=request.user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def recommend(self, request, pk=None):
        """게시글 추천/추천 취소"""
        post = self.get_object()
        user = request.user

        if user in post.recommendations.all():
            post.recommendations.remove(user)  # 이미 추천 → 취소
        else:
            post.recommendations.add(user)  # 추천 추가
            post.dislikes.remove(user)  # 비추천 상태였다면 해제

        return Response(self.get_serializer(post).data)

    @action(detail=True, methods=['post'])
    def dislike(self, request, pk=None):
        """게시글 비추천/비추천 취소"""
        post = self.get_object()
        user = request.user

        if user in post.dislikes.all():
            post.dislikes.remove(user)  # 이미 비추천 → 취소
        else:
            post.dislikes.add(user)  # 비추천 추가
            post.recommendations.remove(user)  # 추천 상태였다면 해제

        return Response(self.get_serializer(post).data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(post_id=self.kwargs.get('post_pk'))

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        serializer.save(author=self.request.user, post=post)
