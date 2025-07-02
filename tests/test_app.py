import unittest
from app import app
import os

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage_loads(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Petri Dish Classifier', response.data)

    def test_upload_invalid_file(self):
        data = {
            'file': (open('app.py', 'rb'), 'app.py')
        }
        response = self.app.post('/predict', data=data, content_type='multipart/form-data')
        self.assertIn(b'Invalid file type', response.data)

    def test_upload_no_file(self):
        response = self.app.post('/predict', data={}, content_type='multipart/form-data')
        self.assertIn(b'No file part in the request.', response.data)

    def test_upload_valid_image(self):
        # Make sure this image exists in your directory for testing
        with open('static/test_images/clean_sample.jpeg', 'rb') as img:
            data = {'file': (img, 'clean_sample.jpeg')}
            response = self.app.post('/predict', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Prediction:', response.data)

if __name__ == '__main__':
    unittest.main()