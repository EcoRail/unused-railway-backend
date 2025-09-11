from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import RailwayProperty
from .serializers import RailwayPropertySerializer

class RailwayPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    철도 유휴부지 목록 및 상세 조회를 위한 API 뷰
    ReadOnlyModelViewSet을 사용하여 조회 기능만 제공합니다.
    """
    queryset = RailwayProperty.objects.all()
    serializer_class = RailwayPropertySerializer
    permission_classes = [permissions.AllowAny] # 누구나 접근 가능