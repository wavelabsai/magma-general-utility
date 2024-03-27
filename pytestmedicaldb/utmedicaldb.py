import unittest
from unittest.mock import patch
from medical_db_api import app


class TestAppointments(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_appointments(self):
        response = self.app.get('/appointments/', auth=('admin', 'password'))
        self.assertEqual(response.status_code, 200)

    def test_get_appointment_by_id(self):
        response = self.app.get('/appointments/4', auth=('dentistjanesmith', 'DrJaneSmith'))
        self.assertEqual(response.status_code, 200)

    @patch('medical_db_api.Appointments.post')
    def test_create_appointment(self, mock_post):
        appointment_data = {
            "doctor_uid": 1,
            "patient_uid": 1,
            "start_time": "2023-01-01T10:00"
        }

        mock_post.return_value = (appointment_data, 200)
        response = self.app.post('/appointments/', auth=('paediatricianjohndoe', 'DrJohnDoe'))
        self.assertEqual(response.status_code, 200)

    @patch('medical_db_api.Appointments.post')
    def test_delete_appointment(self, mock_request):
        response = self.app.delete('/appointments/1', auth=('paediatricianjohndoe', 'DrJohnDoe'))
        self.assertEqual(response.status_code, 200)


class TestDoctors(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_doctors(self):
        response = self.app.get('/doctors/')
        self.assertEqual(response.status_code, 200)

    def test_get_doctor_by_id(self):
        response = self.app.get('/doctors/1')
        self.assertEqual(response.status_code, 200)

    @patch('medical_db_api.Doctors.post')
    def test_create_doctor(self, mock_post):
        doctor = {
            "full name": "Dr Fitzwilliam Darcy",
            "username": "mrdarcy",
            "speciality": "cardiologist",
            "password": "prideandprejudice",
        }

        mock_post.return_value = (doctor, 200)
        response = self.app.post('/doctors/', auth=('admin', 'password'))
        self.assertEqual(response.status_code, 200)


class TestPatients(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_get_patients(self):
        response = self.app.get('/patients/', auth=('admin', 'password'))
        self.assertEqual(response.status_code, 200)

    def test_get_patient_by_id(self):
        response = self.app.get('/appointments/1', auth=('admin', 'password'))
        self.assertEqual(response.status_code, 200)

    @patch('medical_db_api.Patients.post')
    def test_create_patient(self, mock_post):
        patient = {
            "full name": "John Cena",
            "username": "johncena",
            "password": "cantseeme",
            "phone": "1234567890",
            "email": "invisibleman@service.com",
        }

        mock_post.return_value = (patient, 200)
        response = self.app.post('/patients/', auth=('admin', 'password'))
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
