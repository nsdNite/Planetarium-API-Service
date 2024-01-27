from rest_framework.routers import DefaultRouter

from planetarium_api.views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register("astronomyshow", AstronomyShowViewSet)
router.register("showtheme", ShowThemeViewSet)
router.register("planetariumdome", PlanetariumDomeViewSet)
router.register("showsession", ShowSessionViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = router.urls

app_name = "planetarium_api"
