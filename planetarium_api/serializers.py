from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from planetarium_api.models import (
    AstronomyShow,
    PlanetariumDome,
    Reservation,
    ShowSession,
    ShowTheme,
    Ticket
)


class ShowThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = (
            "id",
            "name",
        )


class ShowSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowSession
        fields = (
            "id",
            "astronomy_show",
            "planetarium_dome",
            "show_time",
        )


class ShowSessionListSerializer(ShowSessionSerializer):
    astronomy_show_title = serializers.CharField(
        source="astronomy_show.name",
        read_only=True,
    )
    planetarium_dome_name = serializers.CharField(
        source="planetarium_dome.name",
        read_only=True,
    )
    planetarium_dome_capacity = serializers.IntegerField(
        source="planetarium_dome_capacity",
        read_only=True,
    )
    tickets_available = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show_title",
            "planetarium_dome_name",
            "planetarium_dome_capacity",
            "tickets_available",
        )


class AstronomyShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
        )


class AstronomyShowListSerializer(serializers.ModelSerializer):
    show_theme = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme"
        )


class AstronomyShowDetailSerializer(serializers.ModelSerializer):
    show_theme = ShowThemeSerializer(
        many=True, read_only=True,
    )

    class Meta:
        model = AstronomyShow
        fields = (
            "id",
            "title",
            "description",
            "show_theme",
        )


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity"
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["show_session"].planetarium_dome,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "show_session",
        )


class TicketListSerializer(TicketSerializer):
    show_session = ShowSessionListSerializer(
        many=False,
        read_only=True,
    )


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = (
            "row",
            "seat",
        )


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False
    )

    class Meta:
        model = Reservation
        fields = (
            "id",
            "tickets",
            "created_at",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(
                    reservation=reservation,
                    **ticket_data
                )
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True,
    )


class ShowSessionDetailSerializer(ShowSessionSerializer):
    astronomy_show = AstronomyShowSerializer(
        many=False,
        read_only=True,
    )
    planetarium_dome = PlanetariumDomeSerializer(
        many=False,
        read_only=True,
    )
    taken_place = TicketSeatsSerializer(
        source="tickets",
        many=True,
        read_only=True,
    )

    class Meta:
        model = ShowSession
        fields = (
            "id",
            "show_time",
            "astronomy_show",
            "planetarium_dome",
            "taken_place",
        )
