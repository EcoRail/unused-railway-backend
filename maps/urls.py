from rest_framework.routers import DefaultRouter
from .views import RailwayPropertyViewSet

router = DefaultRouter()
# 'properties'라는 경로로 RailwayPropertyViewSet을 등록합니다.
router.register('properties', RailwayPropertyViewSet) 

urlpatterns = router.urls