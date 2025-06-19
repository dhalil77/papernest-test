from django.test import TestCase

# Create your tests here.
import pytest
import asyncio
from django.test import TestCase, AsyncClient
from django.urls import reverse
from unittest.mock import patch, AsyncMock
from .views import RetrieveCoverageView, init_antennes_data

class CoverageAPITest(TestCase):
    """Tests pour l'API de couverture"""
    
    def setUp(self):
        self.client = AsyncClient()
        self.coverage_url = reverse('coverage')
    
    @pytest.mark.asyncio
    async def test_coverage_endpoint_valid_data(self):
        """Test avec des données valides"""
        payload = {
            "id1": "1 Place Vendôme, 75001 Paris",
            "id2": "Tour Eiffel, Paris"
        }
        
        with patch('your_app.views.init_antennes_data') as mock_init:
            mock_init.return_value = None
            
            response = await self.client.post(
                self.coverage_url,
                data=payload,
                content_type='application/json'
            )
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('id1', data)
        self.assertIn('id2', data)
    
    @pytest.mark.asyncio
    async def test_coverage_endpoint_invalid_data(self):
        """Test avec des données invalides"""
        response = await self.client.post(
            self.coverage_url,
            data="invalid json",
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_coverage_endpoint_empty_data(self):
        """Test avec des données vides"""
        response = self.client.post(
            self.coverage_url,
            data={},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)