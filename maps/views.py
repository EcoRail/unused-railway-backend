from rest_framework import viewsets, permissions, filters
from .models import RailwayProperty
from .serializers import RailwayPropertySerializer

class RailwayPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RailwayProperty.objects.all()
    serializer_class = RailwayPropertySerializer
    permission_classes = [permissions.AllowAny]
    
    # 검색 기능 추가
    filter_backends = [filters.SearchFilter]
    search_fields = ['address', 'line_name', 'regional_headquarters']
