import unittest
import json
from app import app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get_doctors(self):
        response = self.app.get('/doctors/')
        self.assertEqual(response.status_code, 200)

    def test_get_doctor_by_uid(self):
        response = self.app.get('/doctors/1')
        self.assertEqual(response.status_code, 200)

    def test_get_nonexistent_doctor(self):
        response = self.app.get('/doctors/1000')
        self.assertEqual(response.status_code, 400)

    def test_post_doctor(self):
        data = {
            "full name": "Test Doctor",
            "username": "testdoctor",
            "speciality": "test speciality",
            "password": "testpassword"
        }
        response = self.app.post('/doctors/', json=data)
        self.assertEqual(response.status_code, 200)

    # Similarly, you can write tests for other endpoints like Patients and Appointments


if __name__ == '__main__':
    unittest.main()
