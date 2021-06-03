from flask import url_for
from flask_testing import TestCase
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestAPI(TestBase):
    def test_api(self):
        response = self.client.get(url_for('get_country'))
        content = response.data.decode('utf-8')
        country_code = content.split('-')[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(content), str)
        self.assertEqual(len(country_code), 2)