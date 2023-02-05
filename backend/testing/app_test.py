import unittest
from unittest.mock import Mock
import bcrypt
import json
from flask import Flask
from services.admin.audio import addAudio
# from views.user.user import *

app = Flask(__name__)

class TestDemo(unittest.TestCase):
    def setUp(self):
        self.tarckid = 1
        self.title = "Believer"
        self.artist = "sarath"
        self.category = "hip-hop"
        self.album = "Frank Darabont"
        self.image = "https://www.shutterstock.com/shutterstock/photos/1953064195/display_1500/stock-photo--fluorite-oil-painting-conceptual-abstract-picture-of-the-eye-oil-painting-in-colorful-1953064195.jpg"
        self.request = Mock(method='POST')
    def test_demo_success(self):
        with app.app_context():
            response = addAudio(self.tarckid, self.title, self.artist, self.category, self.album,self.image, self.request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {"message": "audio added successfully!"})

    def test_demo_missing_params(self):
        with app.app_context():
            response = addAudio(self.tarckid, "", "", "", "","", self.request)
            self.assertEqual(response.get_json(), {"message": "All fields are required"})
if __name__ == '__main__':
    unittest.main()
