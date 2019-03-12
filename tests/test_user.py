import requests
import unittest
import json
from wenst import creat_app

class TestApi(unittest.TestCase):
    def setUp(self):
        self.app = creat_app('testing')
        self.client = self.app.test_client

        self.user = {
            'name': 'olawale',
            'email': 'olawale@mail.com',
            'password': 'passw0rd!'
        }

        with self.app.app_context():
            db.create_all()

    def test_register(self):
        response = self.client().post('/register',data=json.dump(self.user))
        response_data = json.loads(response.data)
        self.assertEqual(response_data.code, 1)
