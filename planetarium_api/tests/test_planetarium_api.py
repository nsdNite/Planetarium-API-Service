from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

PLANETARIUM_URL = reverse("planetarium_api:astronomyshow-list")
SHOW_SESSION_URL = reverse("planetarium_api:showsession-list")


class UnauthenticatedPlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLANETARIUM_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
