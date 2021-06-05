from flask_testing import TestCase
from flask import url_for
from app import app, db, CovidStats
from requests_mock import mock
import json

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
            m.get("http://country_api:5000/get_country", json={'country_code': 'gb', 'country_name': 'united kingdom'})
            m.post("http://population_api:5000/get_population", json={'population': '65,110,000'})
            m.post('http://stats_api:5000/get_stats', json={'new_cases': 896054, 'ratio': 0.001})

            response = self.client.get(url_for('home'))
            self.assertEqual(response.status_code, 200)

            covid_stats = CovidStats.query.filter_by(id=1).first()
            self.assertEqual(covid_stats.country_code, 'gb')
            self.assertEqual(covid_stats.country_name, 'united kingdom')
            self.assertEqual(covid_stats.population, '65,110,000')
            self.assertEqual(covid_stats.new_cases, '896054')
            self.assertTrue(int(float(covid_stats.ratio)) >= 0)