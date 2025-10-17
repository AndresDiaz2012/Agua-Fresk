from rest_framework.routers import DefaultRouter
from .views import MessageLogViewSet

router = DefaultRouter()
router.register(r'', MessageLogViewSet, basename='messagelog')

urlpatterns = router.urls
