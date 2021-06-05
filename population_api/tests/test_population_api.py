from flask import url_for
from flask_testing import TestCase
import json
import requests_mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestPopulationAPI(TestBase):
    # def test_population_api(self):
    #     response = self.client.post(url_for('get_population'))
    #     self.assertEqual(response.status_code, 200)

    # def test_uk_population(self):

    #     response = self.client.post(url_for('get_population'), data='gb').data.decode('utf-8')
    #     population = int(response.replace(',', ''))
    #     self.assertTrue(population > 65000000)

    # def test_us_population(self):
    #     response = self.client.post(url_for('get_population'), data='us').data.decode('utf-8')
    #     population = int(response.replace(',', ''))
    #     self.assertTrue(population > 320000000)

    # def test_get_population(self):
    #     with requests_mock.Mocker() as mocker:
    #         mocker.post('http://covid-19-app:5000/get_population',json={"country_code":'uk'})

    #     response = self.client.post(url_for('get_population', country_code="uk"))
    #     self.assertEqual(response.status_code, 200)

    def test_get_population(self):
        response = self.client.post(url_for('get_population'), data='gb')
        response_data = response.data.decode('utf-8')
        self.assertEqual(response.status_code, 200)