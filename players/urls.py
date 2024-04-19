from rest_framework.routers import DefaultRouter
from players.views import PlayerViewSet

router = DefaultRouter()
router.register("", PlayerViewSet, basename="players")

urlpatterns = router.urls
