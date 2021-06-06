from flask import url_for
from flask_testing import TestCase
import json
import requests_mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestPopulationAPI(TestBase):
    def test_get_population(self):
        response = self.client.post(url_for('get_population'), data='gb')
        response_data = response.data.decode('utf-8')
        population = int(json.loads(response_data)['population'].replace(',', ''))
        alpha3code = json.loads(response_data)['alpha3code']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(population > 0)
        self.assertEqual(len(alpha3code), 3)