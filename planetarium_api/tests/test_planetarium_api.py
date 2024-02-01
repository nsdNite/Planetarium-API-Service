from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from planetarium_api.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession
)
from planetarium_api.serializers import (
    AstronomyShowSerializer,
    AstronomyShowListSerializer,
    AstronomyShowDetailSerializer
)

SHOW_URL = reverse("planetarium_api:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium_api:showsession-list")


def sample_astronomy_show(**params):
    """Define sample instance of AstronomyShow model"""
    defaults = {
        "title": "Exploring Uranus",
        "description": "I need this joke here, sorry",
    }
    defaults.update(params)

    return AstronomyShow.objects.create(**defaults)


def sample_show_theme(**params):
    """Define sample instance of ShowTheme model"""
    defaults = {
        "name": "History of Spacecraft",
    }
    defaults.update(params)

    return ShowTheme.objects.create(**defaults)


def sample_show_session(**params):
    """Define sample instance of ShowSession model"""
    planetarium_dome = PlanetariumDome.objects.create(
        name="NASA dome", rows=20, seats_in_row=20
    )

    defaults = {
        "astronomy_show ": None,
        "planetarium_dome": planetarium_dome,
        "show_time": "2024-01-02 12:30:00",
    }
    defaults.update(params)

    return ShowSession.objects.create(**defaults)


def detail_url(astronomyshow_id):
    """Retrieve URL of an AstronomyShow instance by id"""
    return reverse(
        "planetarium_api:astronomyshow-detail",
        args=[astronomyshow_id]
    )


class UnauthenticatedPlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test_password12345",
        )
        self.client.force_authenticate(self.user)

    def test_list_astronomy_show(self):
        sample_astronomy_show()

        res = self.client.get(SHOW_URL)

        shows = AstronomyShow.objects.all()
        serializer = AstronomyShowSerializer(shows, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_astronomy_shows_by_title(self):
        show_first = sample_astronomy_show(title="Test 1")
        show_second = sample_astronomy_show(
            title="Test 2: First steps on Moon"
        )
        show_third = sample_astronomy_show(title="REST 3: Life on Mars")

        res = self.client.get(SHOW_URL, {"title": "test"})

        serializer_first = AstronomyShowSerializer(show_first)
        serializer_second = AstronomyShowSerializer(show_second)
        serializer_third = AstronomyShowSerializer(show_third)

        self.assertIn(serializer_first.data, res.data)
        self.assertIn(serializer_second.data, res.data)
        self.assertNotIn(serializer_third.data, res.data)

    def test_filter_show_by_theme(self):
        show_first = sample_astronomy_show(title="Test 1")
        show_second = sample_astronomy_show(
            title="Test 2: First steps on Moon"
        )
        show_third = sample_astronomy_show(title="REST 3: Life on Mars")

        theme_first = sample_show_theme(name="Test Theme 1")
        theme_second = sample_show_theme(name="Test Theme 2")

        show_first.show_themes.add(theme_first)
        show_second.show_themes.add(theme_second)

        res = self.client.get(
            SHOW_URL,
            {
                "show_themes": f"{theme_first.id},{theme_second.id}"
            }
        )
        serializer_first = AstronomyShowListSerializer(show_first)
        serializer_second = AstronomyShowListSerializer(show_second)
        serializer_third = AstronomyShowListSerializer(show_third)

        self.assertIn(serializer_first.data, res.data)
        self.assertIn(serializer_second.data, res.data)
        self.assertNotIn(serializer_third.data, res.data)

    def test_retrieve_show_detail(self):
        show = sample_astronomy_show()
        show.show_themes.add(sample_show_theme())

        url = detail_url(show.id)
        res = self.client.get(url)

        serializer = AstronomyShowDetailSerializer(show)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_movie_forbidden(self):
        payload = {
            "title": "Sample show",
            "description": "Sample description",
        }

        res = self.client.post(SHOW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
