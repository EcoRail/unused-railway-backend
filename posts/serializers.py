from rest_framework import serializers
from .models import Post, Comment
from maps.models import RailwayProperty
from maps.serializers import RailwayPropertySerializer


# 댓글 Serializer
class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'author_username', 'content', 'created_at', 'parent', 'replies']

    def get_replies(self, obj):
        return CommentSerializer(obj.replies.all().order_by('created_at'), many=True, context=self.context).data


# 게시글 생성/수정용 Serializer
class PostCreateUpdateSerializer(serializers.ModelSerializer):
    #railway_property = serializers.PrimaryKeyRelatedField(queryset=RailwayProperty.objects.all())

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'railway_property']


# 게시글 조회용 Serializer
class PostListDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    railway_property_address = serializers.CharField(
        source='railway_property.address',
        read_only=True,
        allow_null=True
    )
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    railway_property_id = serializers.IntegerField(source='railway_property.id', read_only=True)
    is_recommended = serializers.SerializerMethodField()
    is_disliked = serializers.SerializerMethodField()
    recommendation_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'author_username', 'created_at',
            'recommendation_count', 'dislike_count',
            'comments', 'railway_property_address', 'railway_property_id',
            'is_recommended', 'is_disliked', 'status_display'
        ]



    def get_user(self):
        return self.context.get('request').user

    def get_is_recommended(self, obj):
        user = self.get_user()
        if user and user.is_authenticated:
            return obj.recommendations.filter(id=user.id).exists()
        return False

    def get_is_disliked(self, obj):
        user = self.get_user()
        if user and user.is_authenticated:
            return obj.dislikes.filter(id=user.id).exists()
        return False

    def get_recommendation_count(self, obj):
        return obj.recommendations.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()
