from flask import url_for
from flask_testing import TestCase
from requests_mock import mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestStatsAPI(TestBase):
    def test_get_stat(self):
        info = {'country': 'Sri Lanka', 'population': '252000'}
        response = self.client.post(url_for('get_stats'), json=info)
        self.assertEqual(response.status_code, 200)
    
    # def test_stats(self):
    #     response = self.client.post(url_for('get_stats'), json={'country': 'Sri Lanka'})
    #     self.assertTrue(response >= 0)