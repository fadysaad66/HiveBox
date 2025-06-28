"""Unit tests for the temperature API endpoints."""

import unittest
from hivebox_v2 import app

class AppEndpointTests(unittest.TestCase):
    """Test suite for /version and /temperature endpoints."""

    def setUp(self):
        """Set up test client for Flask app."""
        self.client = app.test_client()

    def test_version(self):
        """Test that /version returns status 200 and a version string."""
        response = self.client.get('/version')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('version', data)
        self.assertIsInstance(data['version'], str)

    def test_temperature(self):
        """Test that /temperature returns valid structure or error message."""
        response = self.client.get('/temperature')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'average_temperature' in data or 'message' in data or 'error' in data
        )

if __name__ == '__main__':
    unittest.main()
