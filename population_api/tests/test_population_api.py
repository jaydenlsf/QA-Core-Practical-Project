from flask import url_for
from flask_testing import TestCase
import requests_mock
from app import app

class TestBase(TestCase):
    def create_app(self):
        return app

class TestAPI(TestBase):
    def test_api(self):
        with requests_mock.Mocker() as mocker:
            mocker.get()