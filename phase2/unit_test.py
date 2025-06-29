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
        """Test that /temperature returns a valid response."""
        response = self.client.get('/temperature')
        print("[DEBUG] Response:", response.status_code, response.get_data(as_text=True))

        # Accept either a 200 (success) or 404 (no recent data)
        self.assertIn(response.status_code, [200, 404], msg="Expected 200 or 404 from /temperature")

        if response.status_code == 200:
            data = response.get_json()
            self.assertIn("average_temperature", data)
            self.assertIn("unit", data)

if __name__ == '__main__':
    unittest.main()
