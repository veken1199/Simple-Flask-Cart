from flask_testing import TestCase
from main import create_app, db
from setup import reset_db
from flask import json


class BaseTestCase(TestCase):
    db = None
    client = None

    def create_app(self):
        # pass in test configuration
        app, db = create_app('config.TestingConfig')
        self.db = db
        self.client = app
        reset_db()
        return app

    def setUp(self):
        pass

    def tearDown(self):
        db.session.remove()
        pass

    # helper function to send post request
    def post(self, url, data):
        return self.client.post(url, data=json.dumps(data),
                                content_type='application/json',
                                charset='UTF-8',
                                follow_redirects=True)
