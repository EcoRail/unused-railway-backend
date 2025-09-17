from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """ 사용자 프로필 조회 및 수정을 위한 Serializer """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'phone']
        read_only_fields = ['id']

class RegisterSerializer(serializers.ModelSerializer):
    """ 회원가입을 위한 Serializer """
    # 이메일은 필수 항목으로 지정
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nickname', 'phone']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            nickname=validated_data.get('nickname', ''),
            phone=validated_data.get('phone', '')
        )
        return user
