# users/serializers.py
from rest_framework import serializers
from .models import CustomUser, Proposal



class ProposalSerializer(serializers.ModelSerializer):
    """제안 목록/상세를 위한 시리얼라이저"""
    recommendCount = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Proposal
        fields = ('id', 'title', 'location', 'status', 'recommendCount', 'created_at')

    def get_recommendCount(self, obj):
        return obj.recommended_by.count()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nickname', 'phone', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data['nickname'],
            phone=validated_data.get('phone', None),
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class ProfileSerializer(serializers.ModelSerializer):
    # '나의 제안' 목록 (models.py의 related_name='proposals' 사용)
    my_proposals = ProposalSerializer(source='proposals', many=True, read_only=True)
    
    # '추천한 제안' 목록 (models.py의 related_name='recommended_proposals' 사용)
    recommended = ProposalSerializer(source='recommended_proposals', many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('nickname', 'email', 'my_proposals', 'recommended')