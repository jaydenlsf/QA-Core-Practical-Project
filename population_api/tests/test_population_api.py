from flask import url_for
from flask_testing import TestCase
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestPopulationAPI(TestBase):
    def test_population_api(self):
        response = self.client.post(url_for('get_population'))
        self.assertEqual(response.status_code, 200)

    def test_uk_population(self):
        response = self.client.post(url_for('get_population'), data='gb').data.decode('utf-8')
        population = int(response.replace(',', ''))
        self.assertTrue(population > 65000000)

    def test_us_population(self):
        response = self.client.post(url_for('get_population'), data='us').data.decode('utf-8')
        population = int(response.replace(',', ''))
        self.assertTrue(population > 320000000)