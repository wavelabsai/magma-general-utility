import unittest
import json
from unittest.mock import patch
from medical_db_api import app

class TestAppointments(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_appointments(self):
        response = self.app.get('/appointments/')
        self.assertEqual(response.status_code, 200)

    def test_get_appointment_by_id(self):
        response = self.app.get('/appointments/1')
        self.assertEqual(response.status_code, 200)

    @patch('your_flask_app.request')
    def test_create_appointment(self, mock_request):
        mock_request.get_json.return_value = {
            "doctor_uid": 1,
            "patient_uid": 1,
            "start_time": "2023-01-01T10:00"
        }
        response = self.app.post('/appointments/')
        self.assertEqual(response.status_code, 200)

    @patch('your_flask_app.request')
    def test_delete_appointment(self, mock_request):
        response = self.app.delete('/appointments/1')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
