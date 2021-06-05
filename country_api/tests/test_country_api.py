from flask import url_for
from flask_testing import TestCase
import json
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestAPI(TestBase):
    def test_api(self):
        response = self.client.get(url_for('get_country'))
        response_data = response.data.decode('utf-8')
        # content = response.data.decode('utf-8')
        country_code = json.loads(response_data)['country_code']
        country_name = json.loads(response_data)['country_name']
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(type(content), str)
        self.assertEqual(len(country_code), 2)
        self.assertEqual(type(country_name), str)