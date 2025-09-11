from rest_framework import serializers
from .models import RailwayProperty

class RailwayPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = RailwayProperty
        fields = '__all__' # 모든 필드를 JSON으로 변환