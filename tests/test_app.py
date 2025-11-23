import unittest
from app import app

class BasicTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page(self):
        response = self.app.get('/dashboard')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
