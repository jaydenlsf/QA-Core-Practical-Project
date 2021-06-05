from flask import url_for
from flask_testing import TestCase
import json
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestStatsAPI(TestBase):
    def test_get_stat(self):
        response = self.client.post(url_for('get_stats'), json={'country': 'Sri Lanka', 'population': '252000'})
        response_data = response.data.decode('utf-8')
        new_cases = json.loads(response_data)['new_cases']
        ratio = json.loads(response_data)['ratio']
        self.assertEqual(response.status_code, 200)
    
    
    