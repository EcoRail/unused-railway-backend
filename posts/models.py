from django.db import models
from django.conf import settings
from maps.models import RailwayProperty # maps 앱의 모델을 가져옵니다.

class Post(models.Model):
    STATUS_CHOICES = (
        ('open', '모집중'),
        ('closed', '완료'),
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    railway_property = models.ForeignKey(RailwayProperty, on_delete=models.CASCADE, related_name='posts')
    recommendations = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recommended_posts', blank=True)
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='disliked_posts', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')  # ← 추가
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    """ 게시글에 달리는 댓글 모델 """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
