# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, verbose_name='닉네임')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='전화번호')

    def __str__(self):
        return self.username

class Proposal(models.Model):
    """사용자 제안 모델"""
    STATUS_CHOICES = (
        ('recruiting', '모집중'),
        ('completed', '완료'),
    )

    # 제안 작성자 (User와 1:N 관계)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='proposals')
    
    # 이 제안을 추천한 사람들 (User와 M:N 관계)
    recommended_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='recommended_proposals', blank=True, verbose_name='추천한 사용자')
    
    # 프론트엔드 코드에 맞춘 필드들
    title = models.CharField(max_length=100, verbose_name='제안 제목')
    location = models.CharField(max_length=100, verbose_name='장소')
    content = models.TextField(verbose_name='제안 내용') # 상세보기를 위해 content 필드도 추가
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='recruiting', verbose_name='상태')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username}의 제안: {self.title}'