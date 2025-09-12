from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from posts.views import PostViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)

posts_router = routers.NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentViewSet, basename='post-comments')

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api/auth/', include('accounts.urls')),
    # path('api/posts/', include('posts.urls')),
    # path('api/map/', include('maps.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(posts_router.urls)),
    path('api/auth/', include('accounts.urls')),
    path('api/map/', include('maps.urls')),
]
