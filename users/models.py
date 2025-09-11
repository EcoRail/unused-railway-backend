# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True, verbose_name='닉네임')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='전화번호')

    def __str__(self):
        return self.username