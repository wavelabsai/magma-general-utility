import pytest
import requests
import logging
import json
from datetime import datetime, timedelta

class TestMedicalDB:
    # Basic initialization for prelimernay test
    admin_auth =  ("admin", "password")
    doctor_auth = ("paediatricianjohndoe", "DrJohnDoe")
    patient_auth = ("clientjanedoe", "JaneDoe")
    base_url = "http://medical_db:5000"

    def _check_if_uuid_exists(self, dataset, uuid):
        url = f"{TestMedicalDB.base_url}/{dataset}/{uuid}"
        response = requests.get(url, auth=TestMedicalDB.admin_auth)

        if response.status_code != 200:
            return response.status_code

        # If the status code is 200, we have a successful response,
        # so we can proceed to check if the UUID exists.
        response_dict = response.json()  # Parse JSON response
        if dataset == "appointments":
            unique_id_entries = {entry.get("unique_id") for entry in response_dict if "unique_id" in entry}
            if uuid in unique_id_entries:
                return 200
            else:
                return 404

        # If the dataset is not "appointments", we don't need to perform additional checks,
        # so we return the response status code directly.
        return response.status_code

    # Find the highest uuid among the dataset
    def _find_highest_uuid(self, dataset):
        response = requests.get(f"{self.base_url}/{dataset}", auth=self.admin_auth)
        response.raise_for_status()  # Raises an exception for non-200 status codes

        response_dict = response.json()
        unique_ids = {entry.get("unique_id") for entry in response_dict if "unique_id" in entry}

        if unique_ids:  # Check if there are any unique_ids found
            max_unique_id = max(unique_ids)
            return max_unique_id
        else:
            return None  # Return None if no unique_ids found

    def _collect_username(self, dataset):
       response = requests.get(f"{TestMedicalDB.base_url}/{dataset}", auth=TestMedicalDB.admin_auth)
       assert response.status_code == 200
       response_dict = json.loads(response.text)

       unique_ids = set(entry["unique_id"] for entry in response_dict if "unique_id" in entry)
       list_username = []

       for unique_id_entry in unique_ids:
           response = requests.get(f"{TestMedicalDB.base_url}/doctors/{unique_id_entry}", auth=TestMedicalDB.admin_auth)
           assert response.status_code == 200
           response_dict = json.loads(response.text)
           username = set(entry["username"] for entry in response_dict if "username" in entry)
           list_username.append(username)
    
       return list_username

    def _check_appointment_duration(self, appointment_time):
        # Current time
        current_time = datetime.now()

        # Convert the string to a datetime object
        formatted_time = datetime.strptime(appointment_time, '%Y-%m-%dT%H:%M:%S')

        # Calculate the time difference
        time_difference = current_time - formatted_time

        # Define a timedelta object representing 30 minutes
        thirty_minutes = timedelta(minutes=30)

        # Check if the time difference is more than 30 minutes
        if time_difference > thirty_minutes:
            logging.info("Time difference is more than 30 minutes.")
            return False
        
        return True

    # Generate booking time after 2 days
    def _generate_appointment_time(self):
        # Current time
        current_time = datetime.now()

        # Calculate 2 days after the current time
        two_days_after = current_time + timedelta(days=2)

        # Format the datetime object without hours granularity and with "T" format
        formatted_time = two_days_after.strftime('%Y-%m-%dT%H:%M')

        return formatted_time

    def test_get_doctors(self):
        response = requests.get(f"{TestMedicalDB.base_url}/doctors", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

    # Test case for retrieving a specific doctor's information
    def test_get_doctor_by_id(self):
        status_code = self._check_if_uuid_exists("doctors", 1)
        assert status_code == 200

    # Test case for creating a new doctor profile
    def test_create_doctor(self):
        max_unique_id = self._find_highest_uuid("doctors")

        data = {
            "full name": "Dr. Sarah Connor",
            "username": "sarahconnor",
            "speciality": "gynecologist",
            "password": "Sarah123",
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("doctors", max_unique_id + 1)
        assert status_code == 200

    # Test case for checking if uids can be modified 
    def test_unique_doctor_uids_cannot_be_modified(self):
        max_unique_id = self._find_highest_uuid("doctors")

        # Attempt to modify the UID of the doctor
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json={"unique_id": 1000})
        assert response.status_code == 404

    def test_unique_usernames_across_doctor_and_patient_accounts(client):
        # Create a doctor with a specific username
        data = {
            "full name": "Dr. Strange",
            "username": "unique_strange",
            "speciality": "Test Speciality",
            "password": "test_password"
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        # Attempt to create another doctor with the same username
        data = {
            "full name": "Another Doctor",
            "username": "unique_strange",
            "speciality": "Another Speciality",
            "password": "another_password"
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 400

    # Test case for retrieving patients' information
    def test_get_patients(self):
        response = requests.get(f"{TestMedicalDB.base_url}/patients", auth=TestMedicalDB.doctor_auth)
        assert response.status_code == 200

    # Test case for retrieving a specific patient's information
    def test_get_patient_by_id(self):
        status_code = self._check_if_uuid_exists("patients", 1)
        assert status_code == 200

    # Test case for creating a new patient profile
    def test_create_patient(self):
        max_unique_id = self._find_highest_uuid("patients")
        data = {
            "full name": "John Doe",
            "username": "johndoe",
            "password": "John123",
            "phone": "123456789",
            "email": "john.doe@example.com"
        }
        response = requests.post(f"{TestMedicalDB.base_url}/patients", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("patients", max_unique_id + 1)
        assert status_code == 200

    # Test case for retrieving appointments
    def test_get_appointments(self):
        response = requests.get(f"{TestMedicalDB.base_url}/appointments", auth=TestMedicalDB.doctor_auth)
        assert response.status_code == 200

    # Test case for creating a new appointment by unauthorized doctor
    def test_create_appointment_by_unauthorized_doctor(self):
        max_appt_unique_id = self._find_highest_uuid("appointments")
        max_doctor_unique_id = self._find_highest_uuid("doctors")
        max_patients_unique_id = self._find_highest_uuid("patients")

        get_appoinment_time = self._generate_appointment_time()
        data = {
           "doctor_uid": max_doctor_unique_id,
           "patient_uid": max_patients_unique_id,
           "start_time": get_appoinment_time
        }
        response = requests.post(f"{TestMedicalDB.base_url}/appointments", json=data, auth=TestMedicalDB.doctor_auth)
        assert response.status_code == 404

        status_code = self._check_if_uuid_exists("appointments", max_appt_unique_id + 1)
        assert status_code == 404
 

    # Test case for creating a new appointment by authorized doctor
    def test_create_appointment_by_authorized_doctor(self):
        max_appt_unique_id = self._find_highest_uuid("appointments")

        doc_data = {
            "full name": "Dr. Superman Universe",
            "username": "supermanuniverse",
            "speciality": "anesthesia",
            "password": "test_password",
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=doc_data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
        doctor_unique_id = self._find_highest_uuid("doctors")

        pat_data = {
            "full name": "new patient 1",
            "username": "newpatient1",
            "password": "newpatient1@123",
            "phone": "123456789",
            "email": "newpatient.1@example.com"
        }
        response = requests.post(f"{TestMedicalDB.base_url}/patients", json=pat_data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
        patients_unique_id = self._find_highest_uuid("patients")
 
        get_appoinment_time = self._generate_appointment_time()
        data = {
            "doctor_uid": doctor_unique_id,
            "patient_uid": patients_unique_id,
            "start_time": get_appoinment_time
        }
        response = requests.post(f"{TestMedicalDB.base_url}/appointments", json=data,
                                auth=("supermanuniverse", "test_password"))
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("appointments", max_appt_unique_id + 1)
        assert status_code == 404


    # Test case for deleting an appointment
    def test_delete_appointment_by_doctor(self):

        # Create thew new doctor
        doc_data = {
            "full name": "Dr. Superman Multiverse",
            "username": "supermanmultiverse",
            "speciality": "anesthesia",
            "password": "test_password",
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=doc_data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
        doctor_unique_id = self._find_highest_uuid("doctors")

        # Create thew new patient
        pat_data = {
            "full name": "new patient 2",
            "username": "newpatient2",
            "password": "newpatient2@123",
            "phone": "223456789",
            "email": "newpatient.2@example.com"
        }
        response = requests.post(f"{TestMedicalDB.base_url}/patients", json=pat_data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
        patients_unique_id = self._find_highest_uuid("patients")

        # Create thew new appointment
        get_appoinment_time = self._generate_appointment_time()
        data = {
           "doctor_uid": doctor_unique_id,
           "patient_uid": patients_unique_id,
           "start_time": get_appoinment_time
        }
        response = requests.post(f"{TestMedicalDB.base_url}/appointments", json=data,
                                 auth=("supermanmultiverse", "test_password"))
        assert response.status_code == 200

        max_appt_unique_id = self._find_highest_uuid("appointments")

        response = requests.delete(f"{TestMedicalDB.base_url}/appointments/{max_appt_unique_id}",
                                   auth=("supermanmultiverse", "test_password"))
        assert response.status_code == 200
