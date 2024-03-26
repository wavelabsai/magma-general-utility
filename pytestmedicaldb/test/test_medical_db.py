import pytest
import requests
import logging
import json
from datetime import datetime, timedelta

class TestMedicalDB:

    # List populated with pre-configured data
    admin_auth           =  ("admin", "password")
    list_of_doctors      =  {1: ("paediatricianjohndoe", "DrJohnDoe"),
                             2: ("dentistjanesmith", "DrJaneSmith")}
    list_of_patients     =  {1: ("clientjanedoe", "JaneDoe"),
                             2: ("clientjohnsmith", "JohnSmith")}
    list_of_appointments =  {1 :(1, 1), 2: (1,1), 3: (2,1), 4: (2,2)}
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

        # Find the highest uuid among the dataset
    def _get_list_of_uuids(self, dataset):
        response = requests.get(f"{self.base_url}/{dataset}", auth=self.admin_auth)
        response.raise_for_status()  # Raises an exception for non-200 status codes

        response_dict = response.json()
        unique_ids = {entry.get("unique_id") for entry in response_dict if "unique_id" in entry}

        return unique_ids

    # Test case for creating a new doctor profile
    def _util_doctor_create(self, fullname, username, speciality, password):
        max_unique_id = self._find_highest_uuid("doctors")
        data = {
            "full name": fullname,
            "username": username,
            "speciality": speciality,
            "password": password,
        }
        response = requests.post(f"{TestMedicalDB.base_url}/doctors", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("doctors", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_doctors[max_unique_id+1] = (username, password)
        unique_ids = self._get_list_of_uuids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    def _util_patients_create(self, fullname, username, password, phone, email):
        max_unique_id = self._find_highest_uuid("patients")

        data = {
            "full name": fullname,
            "username": username,
            "password": password,
            "phone": phone,
            "email": email,
        }
        response = requests.post(f"{TestMedicalDB.base_url}/patients", json=data, auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("patients", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_patients[max_unique_id+1] = (username, password)
        unique_ids = self._get_list_of_uuids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    # Test case for creating a new appointment profile
    def _util_appointments_create_by_doctor(self, doctor_uid, patient_uid, docter_username, doctor_password,
                                            appointment_time):
        max_unique_id = self._find_highest_uuid("appointments")

        data = {
           "doctor_uid": doctor_uid,
           "patient_uid": patient_uid,
           "start_time": appointment_time,
        }

        response = requests.post(f"{TestMedicalDB.base_url}/appointments", json=data,
                                 auth=(docter_username, doctor_password))
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("appointments", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_appointments[max_unique_id+1] = (doctor_uid, patient_uid)

    def test_doctor_prefconfigured_data(self):
        response = requests.get(f"{TestMedicalDB.base_url}/doctors", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
            
        unique_ids = self._get_list_of_uuids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    # Test case for creating a new doctor profile
    def test_doctor_create_api(self):
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

        TestMedicalDB.list_of_doctors[max_unique_id+1] = ("sarahconnor", "Sarah123")
        unique_ids = self._get_list_of_uuids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    def test_patient_prefconfigured_data(self):
        response = requests.get(f"{TestMedicalDB.base_url}/patients", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        unique_ids = self._get_list_of_uuids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    # Test case for creating a new patient profile
    def test_patient_create_api(self):
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

        TestMedicalDB.list_of_patients[max_unique_id+1] = ("johndoe", "John123")
        unique_ids = self._get_list_of_uuids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    def test_appointments_prefconfigured_data(self):
        response = requests.get(f"{TestMedicalDB.base_url}/appointments", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

        unique_ids = self._get_list_of_uuids("appointments")
        assert len(unique_ids) == len(TestMedicalDB.list_of_appointments)

    # Test case for creating a new appointment profile
    def test_appointments_create_api(self):
        max_unique_id = self._find_highest_uuid("appointments")
        
        latest_doctor_uuid, latest_doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]
        latest_patient_uuid, latest_patient_value = list(TestMedicalDB.list_of_patients.items())[-1]
        
        data = {
           "doctor_uid": latest_doctor_uuid,
           "patient_uid": latest_patient_uuid,
           "start_time": self._generate_appointment_time()
        }

        response = requests.post(f"{TestMedicalDB.base_url}/appointments", json=data, auth=latest_doctor_value)
        assert response.status_code == 200

        status_code = self._check_if_uuid_exists("appointments", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_appointments[max_unique_id+1] = (latest_doctor_uuid, latest_patient_uuid)
        unique_ids = self._get_list_of_uuids("appointments")
        assert len(unique_ids) == len(TestMedicalDB.list_of_appointments)

    def _util_get_appointment_details(self, response_string):
        pos1 = response_string.find('[') + 1

        assert len(response_string[pos1:-3]) > 0 

        data = eval(response_string[pos1:-3])

        doctor_uid = data['doctor_uid']
        patient_uid = data['patient_uid']

        return doctor_uid, patient_uid

    def test_appointments_single_doctor_dual_patient_same_time(self):

       # Create the doctor
       self._util_doctor_create("Dr. Arnold Sh", "arnoladsh", "cardio", "Arnolad123")
       doctor_uuid, doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]

       # Create the patient 1
       self._util_patients_create("Patient 1", "patient1", "patient123", "1234567", "patient1@xyz.com")
       patient1_uuid, patient1_value = list(TestMedicalDB.list_of_patients.items())[-1]

       # Create appointment for doctor and patient 1
       self._util_appointments_create_by_doctor(doctor_uuid, patient1_uuid,
                                                "arnoladsh", "Arnolad123", 
                                                self._generate_appointment_time())

       # Fetch the appointment details using patient 1
       response = requests.get(f"{TestMedicalDB.base_url}/appointments", auth=patient1_value)
       recvd_doctor_uid, recvd_patient_uid = self._util_get_appointment_details(response.text)

       assert recvd_doctor_uid == doctor_uuid
       assert recvd_patient_uid == patient1_uuid

       # Create the patient 2
       self._util_patients_create("Patient 2", "patient2", "patient321", "4563711", "patient2@xyz.com")
       patient2_uuid, patient2_value = list(TestMedicalDB.list_of_patients.items())[-1]

       # Create appointment for doctor and patient 2
       self._util_appointments_create_by_doctor(doctor_uuid, patient2_uuid,
                                                "arnoladsh", "Arnolad123",
                                                self._generate_appointment_time())

       response = requests.get(f"{TestMedicalDB.base_url}/appointments", auth=patient2_value)
       recvd_doctor_uid, recvd_patient_uid = self._util_get_appointment_details(response.text)
 
       assert recvd_doctor_uid == doctor_uuid
       assert recvd_patient_uid == patient2_uuid
