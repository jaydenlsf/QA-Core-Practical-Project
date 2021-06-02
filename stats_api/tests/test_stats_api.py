from flask import url_for
from flask_testing import TestCase
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestStatsAPI(TestBase):
    def test_stats_api(self):
        response = self.client.post(url_for('get_stats'))
        self.assertEqual(response.status_code, 200)

    def test_uk_stats(self):
        response = self.client.post(url_for('get_stats'), data='uk').data.decode('utf-8')
        stats = int(response.replace(',', ''))
        self.assertTrue(stats >= 0)