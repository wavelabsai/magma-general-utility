"""
Test script for testing a medical database API.

This script contains test cases for verifying the functionality of a medical database API.
It covers testing endpoints for creating doctors, patients, and appointments,
as well as checking various scenarios such as appointments creation with different user credentials,
appointment time validation, and more.

The TestMedicalDB class defines individual test methods to cover different aspects of the API,
such as creating doctor profiles, patient profiles, and appointment profiles.
It also includes utility methods for common operations like finding the highest UUID,
checking if a UUID exists, generating appointment time, etc.
"""

import pytest
import requests
import logging
import json
from datetime import datetime, timedelta


# Collect the username from the dataset (doctor or patients)
def collect_username(dataset):
    """
    Collects usernames from a dataset of medical records.

    Args:
        dataset (str): The name of the dataset to collect usernames from.

    Returns:
        list: A list containing unique usernames extracted from the dataset.

    Raises:
        AssertionError: If the HTTP status code of the response is not 200.
    """
    response = requests.get(
                 f"{TestMedicalDB.base_url}/{dataset}", auth=TestMedicalDB.admin_auth
               )
    assert response.status_code == 200
    response_dict = json.loads(response.text)

    unique_ids = set(
            entry["unique_id"] for entry in response_dict if "unique_id" in entry
    )
    list_username = []

    for unique_id_entry in unique_ids:
        response = requests.get(
                f"{TestMedicalDB.base_url}/doctors/{unique_id_entry}",
                auth=TestMedicalDB.admin_auth)

        assert response.status_code == 200
        response_dict = json.loads(response.text)
        username = set(
                entry["username"] for entry in response_dict if "username" in entry
        )
        list_username.append(username)

    return list_username

# Generate booking time after 2 days
def generate_appointment_time():
    """
    Generate an appointment time 2 days after the current time.

    Returns:
        str: A formatted string representing the appointment time in
             ISO 8601 format (YYYY-MM-DDTHH:MM).
    """
    # Current time
    current_time = datetime.now()

    # Calculate 2 days after the current time
    two_days_after = current_time + timedelta(days=2)

    # Format the datetime object without hours granularity and with "T" format
    formatted_time = two_days_after.strftime("%Y-%m-%dT%H:%M")

    return formatted_time

#Check if the given UUID exists (for doctor, patients or appointments)
def check_if_uid_exists(dataset, uid):
    """
    Checks if a unique identifier (UID) exists in the specified dataset.

    Parameters:
    dataset (str): The name of the dataset to search for the UID.
    uid (str): The unique identifier (UID) to check for existence.

    Returns:
    int: The HTTP status code indicating the result of the check.
         - 200 if the UID exists in the dataset.
         - 404 if the UID does not exist in the dataset.
         - Other status codes indicate an error occurred during the request.
    """
    url = f"{TestMedicalDB.base_url}/{dataset}/{uid}"
    response = requests.get(url, auth=TestMedicalDB.admin_auth)

    if response.status_code != 200:
        return response.status_code

    # If the status code is 200, we have a successful response,
    # so we can proceed to check if the UUID exists.
    response_dict = response.json()  # Parse JSON response
    if dataset == "appointments":
        unique_id_entries = {
                entry.get("unique_id")
                for entry in response_dict
                if "unique_id" in entry
        }
        if uid in unique_id_entries:
            return 200

        return 404

    # If the dataset is not "appointments", we don't need to perform additional checks,
    # so we return the response status code directly.
    return response.status_code


class TestMedicalDB:
    """
    Test class for the medical database API.

    This class contains test methods to verify the functionality of the medical database API.
    It includes test cases for creating doctor profiles, patient profiles, and appointment profiles.

    Attributes:
        admin_auth (tuple): Tuple containing admin username and password for API authentication.
        list_of_doctors (dict): Dictionary containing pre-configured doctor data.
        list_of_patients (dict): Dictionary containing pre-configured patient data.
        list_of_appointments (dict): Dictionary containing pre-configured appointment data.
        base_url (str): Base URL of the medical database API.
    """

    # List populated with pre-configured data
    admin_auth = ("admin", "password")
    list_of_doctors = {
        1: ("paediatricianjohndoe", "DrJohnDoe"),
        2: ("dentistjanesmith", "DrJaneSmith"),
    }
    list_of_patients = {
        1: ("clientjanedoe", "JaneDoe"),
        2: ("clientjohnsmith", "JohnSmith"),
    }
    list_of_appointments = {1: (1, 1), 2: (1, 1), 3: (2, 1), 4: (2, 2)}
    base_url = "http://medcial_db:5000"

    # Find the highest uid among the dataset
    def _find_highest_uid(self, dataset):
        response = requests.get(f"{self.base_url}/{dataset}", auth=self.admin_auth)
        response.raise_for_status()  # Raises an exception for non-200 status codes

        response_dict = response.json()
        unique_ids = {
            entry.get("unique_id") for entry in response_dict if "unique_id" in entry
        }

        if unique_ids:  # Check if there are any unique_ids found
            max_unique_id = max(unique_ids)
            return max_unique_id

        return None  # Return None if no unique_ids found

    # Find the highest uid among the dataset
    def _get_list_of_uids(self, dataset):
        response = requests.get(f"{self.base_url}/{dataset}", auth=self.admin_auth)
        response.raise_for_status()  # Raises an exception for non-200 status codes

        response_dict = response.json()
        unique_ids = {
            entry.get("unique_id") for entry in response_dict if "unique_id" in entry
        }

        return unique_ids

    # Test case for creating a new doctor profile
    def _util_doctor_create(self, fullname, username, speciality, password):
        max_unique_id = self._find_highest_uid("doctors")
        data = {
            "full name": fullname,
            "username": username,
            "speciality": speciality,
            "password": password,
        }
        response = requests.post(
            f"{TestMedicalDB.base_url}/doctors",
            json=data,
            auth=TestMedicalDB.admin_auth,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("doctors", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_doctors[max_unique_id + 1] = (username, password)
        unique_ids = self._get_list_of_uids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    def _util_patients_create(self, fullname, username, password, phone, email):
        max_unique_id = self._find_highest_uid("patients")

        data = {
            "full name": fullname,
            "username": username,
            "password": password,
            "phone": phone,
            "email": email,
        }
        response = requests.post(
            f"{TestMedicalDB.base_url}/patients",
            json=data,
            auth=TestMedicalDB.admin_auth,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("patients", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_patients[max_unique_id + 1] = (username, password)
        unique_ids = self._get_list_of_uids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    # Test case for creating a new appointment profile
    def _util_appointments_create(
        self, doctor_uid, patient_uid, auth_username, auth_password, appointment_time
    ):
        max_unique_id = self._find_highest_uid("appointments")

        data = {
            "doctor_uid": doctor_uid,
            "patient_uid": patient_uid,
            "start_time": appointment_time,
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=(auth_username, auth_password),
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_appointments[max_unique_id + 1] = (
            doctor_uid,
            patient_uid,
        )

    def test_doctor_prefconfigured_data(self):
        response = requests.get(
            f"{TestMedicalDB.base_url}/doctors", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    # Test case for creating a new doctor profile
    def test_doctor_create_api(self):
        max_unique_id = self._find_highest_uid("doctors")
        data = {
            "full name": "Dr. Sarah Connor",
            "username": "sarahconnor",
            "speciality": "gynecologist",
            "password": "Sarah123",
        }
        response = requests.post(
            f"{TestMedicalDB.base_url}/doctors",
            json=data,
            auth=TestMedicalDB.admin_auth,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("doctors", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_doctors[max_unique_id + 1] = ("sarahconnor", "Sarah123")
        unique_ids = self._get_list_of_uids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    def test_unique_uids_cannot_be_modified(self):
        # Create a doctor
        self._util_doctor_create("Dr. Hulk", "unique_hulk", "gaestro", "hulk123")
        doctor_uid, doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]

        response = requests.get(
            f"{TestMedicalDB.base_url}/doctors/{doctor_uid}",
            auth=TestMedicalDB.admin_auth,
        )
        assert response.status_code == 200

        doctor_data = json.loads(response.text)[0]
        doctor_uid = doctor_data["unique_id"]

        # Attempt to modify the UID of the doctor
        response = requests.post(
            f"{TestMedicalDB.base_url}/doctors/{doctor_uid}",
            json={"unique_id": 1000},
            auth=TestMedicalDB.admin_auth,
        )

        res = requests.get(f"{TestMedicalDB.base_url}/doctors/{doctor_uid}")
        assert res.status_code == 200

    def test_patient_prefconfigured_data(self):
        response = requests.get(
            f"{TestMedicalDB.base_url}/patients", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    # Test case for creating a new patient profile
    def test_patient_create_api(self):
        max_unique_id = self._find_highest_uid("patients")
        data = {
            "full name": "John Doe",
            "username": "johndoe",
            "password": "John123",
            "phone": "123456789",
            "email": "john.doe@example.com",
        }
        response = requests.post(
            f"{TestMedicalDB.base_url}/patients",
            json=data,
            auth=TestMedicalDB.admin_auth,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("patients", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_patients[max_unique_id + 1] = ("johndoe", "John123")
        unique_ids = self._get_list_of_uids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    def test_appointments_prefconfigured_data(self):
        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("appointments")
        assert len(unique_ids) == len(TestMedicalDB.list_of_appointments)

    # Test case for creating a new appointment profile
    def test_appointments_create_api(self):
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": generate_appointment_time(),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code == 200

        TestMedicalDB.list_of_appointments[max_unique_id + 1] = (
            latest_doctor_uid,
            latest_patient_uid,
        )
        unique_ids = self._get_list_of_uids("appointments")
        assert len(unique_ids) == len(TestMedicalDB.list_of_appointments)

    def _util_get_appointment_details(self, response_string):
        pos1 = response_string.find("[") + 1

        assert len(response_string[pos1:-3]) > 0

        data = eval(response_string[pos1:-3])

        doctor_uid = data["doctor_uid"]
        patient_uid = data["patient_uid"]

        return doctor_uid, patient_uid

    def test_appointments_single_doctor_dual_patient_same_time_by_doctor_cred(self):

        # Create the doctor
        self._util_doctor_create("Dr. Arnold Sh", "arnoladsh", "cardio", "Arnolad123")
        doctor_uid, doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]

        # Create the patient 1
        self._util_patients_create(
            "Patient 1", "patient1", "patient123", "1234567", "patient1@xyz.com"
        )
        patient1_uid, patient1_value = list(TestMedicalDB.list_of_patients.items())[-1]

        # Create appointment for doctor and patient 1
        self._util_appointments_create(
            doctor_uid,
            patient1_uid,
            "arnoladsh",
            "Arnolad123",
            generate_appointment_time(),
        )

        # Fetch the appointment details using patient 1
        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=patient1_value
        )
        recvd_doctor_uid, recvd_patient_uid = self._util_get_appointment_details(
            response.text
        )

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == patient1_uid

        # Create the patient 2
        self._util_patients_create(
            "Patient 2", "patient2", "patient321", "4563711", "patient2@xyz.com"
        )
        patient2_uid, patient2_value = list(TestMedicalDB.list_of_patients.items())[-1]

        # Create appointment for doctor and patient 2
        self._util_appointments_create(
            doctor_uid,
            patient2_uid,
            "arnoladsh",
            "Arnolad123",
            generate_appointment_time(),
        )

        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=patient2_value
        )
        recvd_doctor_uid, recvd_patient_uid = self._util_get_appointment_details(
            response.text
        )

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == patient2_uid

    def test_appointments_single_patient_dual_doctor_same_time_by_doctor_cred(self):

        # Create the doctor Strange
        self._util_doctor_create(
            "Dr. Strange 1", "drstrangeavenger", "mystical", "StrangeAvenger1"
        )
        doctor_strange_uid, doctor_strange_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]

        # Create the Single Patient 1
        self._util_patients_create(
            "Single Patient 1",
            "singlepatient",
            "SinglePatient123",
            "3456789",
            "strangeavenger1@xyz.com",
        )
        single_patient_uid, single_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        # Create appointment for doctor strange and single patient 1
        self._util_appointments_create(
            doctor_strange_uid,
            single_patient_uid,
            "drstrangeavenger",
            "StrangeAvenger1",
            generate_appointment_time(),
        )

        # Create the doctor Strange New
        self._util_doctor_create(
            "Dr. Strange 2", "drstrangeavengernew", "mysticalnew", "StrangeAvengerNew"
        )
        doctor_strange_new_uid, doctor_strange_new_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]

        # Create appointment for doctor and patient 2
        self._util_appointments_create(
            doctor_strange_new_uid,
            single_patient_uid,
            "drstrangeavengernew",
            "StrangeAvengerNew",
            generate_appointment_time(),
        )

        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=single_patient_value
        )
        assert response.status_code != 200

    def test_appointments_single_doctor_single_patient_by_patient_cred(self):

        # Create the doctor
        self._util_doctor_create(
            "Dr. DoLittle ", "dolittle", "veteneray", "DoLittle123"
        )
        doctor_uid, doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]

        # Create the patient parrot
        self._util_patients_create(
            "Patient Parrot",
            "patientparrot",
            "parrot123",
            "123452267",
            "parrot1241@xyz.com",
        )
        parrot_uid, parrot_value = list(TestMedicalDB.list_of_patients.items())[-1]

        # Create appointment for doctor and patient parrot
        self._util_appointments_create(
            doctor_uid,
            parrot_uid,
            "patientparrot",
            "parrot123",
            generate_appointment_time(),
        )

        # Fetch the appointment details using patient parrot
        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=parrot_value
        )
        recvd_doctor_uid, recvd_patient_uid = self._util_get_appointment_details(
            response.text
        )

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == parrot_uid

    # Test case for creating a new appointment profile with wrong time format
    def test_appointments_create_api_with_wrong_appointment_time_format(self):
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment profile with 30 minute time gap
    def test_appointments_create_api_with_30_minute_gap_in_appointment_time(self):
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_date_time = datetime.now()

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_date_time.strftime("%Y-%m-%dT%H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code == 200

        new_date_time = current_date_time + timedelta(minutes=30)
        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": new_date_time.strftime("%Y-%m-%dT%H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("appointments", max_unique_id + 2)
        assert status_code == 200
