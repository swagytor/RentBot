from rest_framework.routers import DefaultRouter

from courts.views import CourtViewSet

router = DefaultRouter()
router.register("", CourtViewSet, basename="courts")

urlpatterns = router.urls
