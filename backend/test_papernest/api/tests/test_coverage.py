from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class CoverageAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('coverage')  

    def test_valid_addresses(self):
        data = {
            "id1": "157 boulevard Mac Donald 75019 Paris",
            "id2": "5 avenue Anatole France 75007 Paris"
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("id1", response.data)
        self.assertIn("id2", response.data)

    def test_invalid(self):
        data = "invalid payload"
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_empty(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
