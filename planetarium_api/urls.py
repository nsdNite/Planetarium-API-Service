from rest_framework.routers import DefaultRouter

from planetarium_api.views import (
    AstronomyShowViewSet,
    ShowThemeViewSet,
    PlanetariumDomeViewSet,
    ShowSessionViewSet,
    TicketViewSet,
    ReservationViewSet,
)

router = DefaultRouter()
router.register("astronomy-show", AstronomyShowViewSet)
router.register("show-theme", ShowThemeViewSet)
router.register("planetarium-dome", PlanetariumDomeViewSet)
router.register("show-session", ShowSessionViewSet)
router.register("ticket", TicketViewSet)
router.register("reservation", ReservationViewSet)

urlpatterns = router.urls

app_name = "planetarium_api"
