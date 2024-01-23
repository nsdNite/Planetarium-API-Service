from rest_framework import viewsets

from planetarium_api.models import (
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    ShowSession,
    ShowTheme,
    Ticket
)

from planetarium_api.serializers import (
    ShowThemeSerializer,
    ShowSessionSerializer,
    AstronomyShowSerializer,
    PlanetariumDomeSerializer,
    TicketSerializer,
    ReservationSerializer,
)


class AstronomyShowViewSet(viewsets.ModelViewSet):
    queryset = AstronomyShow.objects.all()
    serializer_class = AstronomyShowSerializer


class ShowThemeViewSet(viewsets.ModelViewSet):
    queryset = ShowTheme.objects.all()
    serializer_class = ShowThemeSerializer


class PlanetariumDomeViewSet(viewsets.ModelViewSet):
    queryset = PlanetariumDome.objects.all()
    serializer_class = PlanetariumDomeSerializer


class ShowSessionViewSet(viewsets.ModelViewSet):
    queryset = ShowSession.objects.all()
    serializer_class = ShowSessionSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
