from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """ 사용자 프로필 조회 및 수정을 위한 Serializer """
    class Meta:
        model = User
        # 비밀번호는 보여주지 않고, id, 이름, 이메일만 다룹니다.
        fields = ['id', 'username', 'email']
        read_only_fields = ['id'] # id는 읽기만 가능

class RegisterSerializer(serializers.ModelSerializer):
    """ 회원가입을 위한 Serializer """
    # 이메일은 필수 항목으로 지정
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # email 필드가 validated_data에 포함되도록 수정
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
