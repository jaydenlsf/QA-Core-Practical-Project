from flask_testing import TestCase
from flask import url_for
from app import app, db
from requests_mock import mock

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            DEBUG=True
        )
        return app

    def setUp(self):
        db.create_all()
    
    def tearDown(self):
        db.drop_all()

class TestHome(TestBase):
    def test_home(self):
        with mock() as m:
            m.get("http://country_api:5000/get_country", text='gb-united kingdom')
            m.post("http://population_api:5000/get_population", text='65,110,000')
            m.post('http://stats_api:5000/get_stats', json={'new_cases': 896054, 'percentage': 0.000009})

            response = self.client.get(url_for('home'))
            self.assertEqual(response.status_code, 200)
            