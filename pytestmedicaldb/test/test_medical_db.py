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

from datetime import datetime, timedelta
import json
import requests


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
            auth=TestMedicalDB.admin_auth,
        )

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


# Check if the given UUID exists (for doctor, patients or appointments)
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
            entry.get("unique_id") for entry in response_dict if "unique_id" in entry
        }
        if uid in unique_id_entries:
            return 200

        return 404

    # If the dataset is not "appointments", we don't need to perform additional checks,
    # so we return the response status code directly.
    return response.status_code


def get_appointment_details(response_string):
    pos1 = response_string.find("[") + 1

    assert len(response_string[pos1:-3]) > 0

    data = eval(response_string[pos1:-3])

    doctor_uid = data["doctor_uid"]
    patient_uid = data["patient_uid"]
    appointment_uid = data["unique_id"]

    return doctor_uid, patient_uid, appointment_uid


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
    base_url = "http://medical_db:5000"

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
        """
        Test case to verify if the endpoint for retrieving doctors' data
        with preconfigured data works as expected.

        This test performs the following steps:
          1. Sends a GET request to the '/doctors' endpoint with admin authentication.
          2. Checks if the response status code is 200 (OK).
          3. Retrieves the list of unique IDs for doctors from the database.
          4. Compares the length of unique IDs obtained from the database
             with the length of preconfigured list of doctors.

        Returns:
           None: This test does not return anything. It asserts conditions
                 to ensure the correctness of the functionality being tested.
        """
        response = requests.get(
            f"{TestMedicalDB.base_url}/doctors", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("doctors")
        assert len(unique_ids) == len(TestMedicalDB.list_of_doctors)

    # Test case for creating a new doctor profile
    def test_doctor_create_api(self):
        """
        Test case to verify the functionality of creating a new doctor via the API.

        This test performs the following steps:
          1. Retrieves the highest unique ID currently assigned to doctors in the database.
          2. Constructs data for creating a new doctor, including full name, username,
             specialty, and password.
          3. Sends a POST request to the '/doctors' endpoint with the constructed data
             and admin authentication.
          4. Asserts that the response status code is 200 (OK).
          5. Verifies if the newly created doctor's unique ID exists in the database.
          6. Adds the newly created doctor to the preconfigured list of doctors.
          7. Retrieves the list of unique IDs for doctors from the database and compares
             it with the updated list of preconfigured doctors.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
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

    def test_patient_prefconfigured_data(self):
        """
        Test case to verify if the endpoint for retrieving patients' data
        with preconfigured data works as expected.

        This test performs the following steps:
          1. Sends a GET request to the '/patients' endpoint with admin authentication.
          2. Checks if the response status code is 200 (OK).
          3. Retrieves the list of unique IDs for patients from the database.
          4. Compares the length of unique IDs obtained from the database
             with the length of preconfigured list of patients.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
        response = requests.get(
            f"{TestMedicalDB.base_url}/patients", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("patients")
        assert len(unique_ids) == len(TestMedicalDB.list_of_patients)

    # Test case for creating a new patient profile
    def test_patient_create_api(self):
        """
        Test case to verify the functionality of creating a new patient via the API.

        This test performs the following steps:
          1. Retrieves the highest unique ID currently assigned to patients in the database.
          2. Constructs data for creating a new patient, including full name, username,
             password, phone number, and email.
          3. Sends a POST request to the '/patients' endpoint with the constructed data
             and admin authentication.
          4. Asserts that the response status code is 200 (OK).
          5. Verifies if the newly created patient's unique ID exists in the database.
          6. Adds the newly created patient to the preconfigured list of patients.
          7. Retrieves the list of unique IDs for patients from the database and compares
             it with the updated list of preconfigured patients.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
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
        """
        Test case to verify if the endpoint for retrieving appointments' data
        with preconfigured data works as expected.

        This test performs the following steps:
          1. Sends a GET request to the '/appointments' endpoint with admin authentication.
          2. Checks if the response status code is 200 (OK).
          3. Retrieves the list of unique IDs for appointments from the database.
          4. Compares the length of unique IDs obtained from the database
             with the length of preconfigured list of appointments.

        Returns:
           None: This test does not return anything. It asserts conditions
                 to ensure the correctness of the functionality being tested.
        """
        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=TestMedicalDB.admin_auth
        )
        assert response.status_code == 200

        unique_ids = self._get_list_of_uids("appointments")
        assert len(unique_ids) == len(TestMedicalDB.list_of_appointments)

    # Test case for creating a new appointment profile
    def test_appointments_create_api(self):
        """
        Test case to verify the functionality of creating a new appointment via the API.

        This test performs the following steps:
          1. Retrieves the highest unique ID currently assigned to appointments in the database.
          2. Retrieves the UID and authentication details of the latest doctor and patient
             from the preconfigured data.
          3. Constructs data for creating a new appointment, including doctor UID, patient UID,
             and appointment start time.
          4. Sends a POST request to the '/appointments' endpoint with the constructed data
             and the latest doctor's authentication details.
          5. Asserts that the response status code is 200 (OK).
          6. Verifies if the newly created appointment's unique ID exists in the database.
          7. Adds the newly created appointment to the preconfigured list of appointments.
          8. Retrieves the list of unique IDs for appointments from the database and compares
             it with the updated list of preconfigured appointments.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

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

    def test_appointments_single_doctor_dual_patient_same_time_by_doctor_cred(self):
        """Test creating appointments for a single doctor with two different patients at the
           same time using doctor credentials.

        This method tests the functionality of creating appointments for a single doctor with 
        two different patients at the same time using doctor credentials. It performs the following steps:

        1. Creates a doctor with the name "Dr. Arnold Sh" and credentials "arnoladsh", "cardio", and "Arnolad123".
        2. Retrieves the UID of the created doctor.
        3. Creates the first patient with the name "Patient 1" and credentials "patient1", "patient123", "1234567", and "patient1@xyz.com".
        4. Retrieves the UID and authentication value of the first patient.
        5. Creates an appointment for the doctor and the first patient.
        6. Fetches appointment details using the credentials of the first patient.
        7. Parses the response to get the doctor UID, patient UID, and appointment ID.
        8. Asserts that the received doctor UID matches the originally created doctor UID.
        9. Asserts that the received patient UID matches the UID of the first patient.
        10. Asserts that a non-zero appointment ID is received.
        11. Creates the second patient with the name "Patient 2" and credentials "patient2", "patient321", "4563711", and "patient2@xyz.com".
        12. Retrieves the UID and authentication value of the second patient.
        13. Creates an appointment for the doctor and the second patient.
        14. Fetches appointment details using the credentials of the second patient.
        15. Parses the response to get the doctor UID, patient UID, and appointment ID.
        16. Asserts that the received doctor UID matches the originally created doctor UID.
        17. Asserts that the received patient UID matches the UID of the second patient.
        18. Asserts that a non-zero appointment ID is received.

        Raises:
           AssertionError: If any of the assertions fail.
        """
        # Create the doctor
        self._util_doctor_create("Dr. Arnold Sh", "arnoladsh", "cardio", "Arnolad123")
        doctor_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

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
        (
            recvd_doctor_uid,
            recvd_patient_uid,
            recvd_appointment_id,
        ) = get_appointment_details(response.text)

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == patient1_uid
        assert recvd_appointment_id != 0

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
        (
            recvd_doctor_uid,
            recvd_patient_uid,
            recvd_appointment_id,
        ) = get_appointment_details(response.text)

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == patient2_uid
        assert recvd_appointment_id != 0

    def test_appointments_single_patient_dual_doctor_same_time_by_doctor_cred(self):
        """
        Test case to verify the scenario where a single doctor has appointments
        scheduled with two different patients at the same time using the doctor's credentials.

        This test performs the following steps:
          1. Creates a new doctor.
          2. Creates a new patient 1.
          3. Creates an appointment for the doctor and patient 1.
          4. Retrieves the appointment details using patient 1's credentials and verifies the doctor
             UID and patient UID.
          5. Creates a new patient 2.
          6. Creates an appointment for the doctor and patient 2.
          7. Retrieves the appointment details using patient 2's credentials and verifies the doctor
              UID and patient UID.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
        # Create the doctor Strange
        self._util_doctor_create(
            "Dr. Strange 1", "drstrangeavenger", "mystical", "StrangeAvenger1"
        )
        doctor_strange_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

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
        doctor_strange_new_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

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
        """Test fetching appointments for a single doctor and a single patient using patient credentials.

        This method tests the functionality of fetching appointments for a single doctor and a single patient using patient credentials. It performs the following steps:

          1. Creates a doctor with the name "Dr. DoLittle" and credentials "dolittle", "veteneray", and "DoLittle123".
          2. Retrieves the UID and authentication value of the created doctor.
          3. Creates a patient named "Patient Parrot" with credentials "patientparrot", "parrot123", "123452267", and "parrot1241@xyz.com".
          4. Retrieves the UID and authentication value of the created patient.
          5. Creates an appointment for the created doctor and patient.
          6. Fetches appointment details using the patient's credentials.
          7. Parses the response to get the doctor UID, patient UID, and appointment ID.
          8. Asserts that the received doctor UID matches the originally created doctor UID.
          9. Asserts that the received patient UID matches the originally created patient UID.
          10. Asserts that a non-zero appointment ID is received.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        # Create the doctor
        self._util_doctor_create(
            "Dr. DoLittle ", "dolittle", "veteneray", "DoLittle123"
        )
        doctor_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

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
        (
            recvd_doctor_uid,
            recvd_patient_uid,
            recvd_appointment_id,
        ) = get_appointment_details(response.text)

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == parrot_uid
        assert recvd_appointment_id != 0

    # Test case for creating a new appointment profile with wrong time format
    def test_appointments_create_api_with_wrong_appointment_time_format(self):
        """Test creating a new appointment profile with a wrong appointment time format.

        This method tests the functionality of creating a new appointment profile with a wrong
        appointment time format. It performs the following steps:

          1. Determines the highest UID currently existing in the "appointments" database table.
          2. Retrieves the UID and authentication value of the latest doctor and patient in the database.
          3. Retrieves the current date and time.
          4. Constructs data for the appointment creation with the doctor UID, patient UID, and a wrongly formatted date and time where the time is represented in 24-hour format (e.g., "14:30:00" for 2:30 PM).
          5. Sends a POST request to create the appointment with the constructed data, authenticated with the doctor's credentials.
          6. Asserts that the response status code is 400, indicating a bad request due to the wrong format.
          7. Checks if the UID of the newly created appointment does not exist in the "appointments" table.

        Raises:
           AssertionError: If any of the assertions fail.
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

        current_date_time = datetime.now()

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_date_time.strftime("%Y-%m-%dT%H:%M:%S"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment with wrong year format
    def test_appointments_create_api_with_wrong_appointment_year_format(self):
        """Test creating a new appointment profile with a wrong appointment year format.

        This method tests the functionality of creating a new appointment profile with a wrong
        appointment year format. It performs the following steps:

          1. Determines the highest UID currently existing in the "appointments" database table.
          2. Retrieves the UID and authentication value of the latest doctor and patient in the database.
          3. Retrieves the current date and time.
          4. Constructs data for the appointment creation with the doctor UID, patient UID, and a
             wrongly formatted date and time where the year is represented in two digits (e.g., "21" for 2021).
          5. Sends a POST request to create the appointment with the constructed data, authenticated with the doctor's credentials.
          6. Asserts that the response status code is 400, indicating a bad request due to the wrong format.
          7. Checks if the UID of the newly created appointment does not exist in the "appointments" table.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

        current_date_time = datetime.now()

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_date_time.strftime("%y-%m-%dT%H:%M:%S"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment with wrong month format
    def test_appointments_create_api_with_wrong_appointment_month_format(self):
        """Test creating a new appointment profile with a wrong appointment month format.

        This method tests the functionality of creating a new appointment profile with a wrong
        appointment month format. It performs the following steps:

          1. Determines the highest UID currently existing in the "appointments" database table.
          2. Retrieves the UID and authentication value of the latest doctor and patient in the database.
          3. Retrieves the current date and time.
          4. Constructs data for the appointment creation with the doctor UID, patient UID, and a wrongly
             formatted date and time where the month is represented as abbreviated text (e.g., "Jan", "Feb", etc.).
          5. Sends a POST request to create the appointment with the constructed data, authenticated with
             the doctor's credentials.
          6. Asserts that the response status code is 400, indicating a bad request due to the wrong format.
          7. Checks if the UID of the newly created appointment does not exist in the "appointments" table.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

        current_date_time = datetime.now()

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_date_time.strftime("%Y-%b-%dT%H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200
# Test case for creating a new appointment with wrong single digit month format
    def test_appointments_create_api_with_wrong_appointment_single_digit_month_format(self):
        """
        Test case to verify the behavior of the appointments creation API
        when providing a single-digit month format in the appointment start time.

        This test case checks if the API returns a 400 status code when an
        appointment is attempted to be created with a single-digit month format
        in the appointment start time.

        Args:
            self: Instance of the test class.

        Returns:
            None
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()
        # Modify the date to a single digit Month
        current_dateTime  = current_dateTime.replace(month=3)

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%-m-%dT%H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200


    # Test case for creating a new appointment with wrong date with single digit daay format
    def test_appointments_create_api_with_wrong_appointment_single_digit_day_format(self):
        """
        Test case for creating an appointment API with a single-digit day format.

        This test case verifies the behavior of the appointments creation API endpoint
        when provided with a wrong single-digit day format in the appointment start time.

        It attempts to create a new appointment using the provided data and checks whether
        the API returns the expected HTTP status code 400.

        It also verifies that the appointment with the expected UID does not exist in the
        database after the API call.

        Raises:
            AssertionError: If the API response status code is not 400 or if the
                            appointment with the expected UID exists in the database.
        """  
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()
        # Modify the date to a single digit day
        current_dateTime  = current_dateTime.replace(day=5)

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%m-%-dT%H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment with wrong single digit hour format
    def test_appointments_create_api_with_wrong_appointment_single_digit_hour_format(self):
        """
        Test case to verify the behavior of creating appointments with an incorrect appointment time format,
        specifically when the hour part of the appointment time is a single digit.

        This test performs the following steps:
        1. Finds the highest unique ID for appointments in the database.
        2. Retrieves the details of the latest doctor and patient.
        3. Modifies the current date-time to set the hour value to 5 for validation purposes.
        4. Constructs appointment data with the latest doctor and patient details and the modified appointment time.
        5. Sends a POST request to the appointments API endpoint with the constructed data.
        6. Asserts that the response status code is 400, indicating a bad request due to incorrect time format.
        7. Checks if the UID exists for the appointment created with the next unique ID.
        8. Asserts that the status code for UID existence check is not 200, indicating failure.

        This test ensures that the API rejects appointments with an incorrect time format,
        particularly when the hour part is a single digit.

        :param self: Instance of the test case class.
        :return: None
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()
        # Modify the hour value in current date to validate
        current_dateTime  = current_dateTime.replace(hour=5)

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%m-%-dT%-H:%M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment with wrong single digit minute format
    def test_appointments_create_api_with_wrong_appointment_single_digit_minute_format(self):
        """
        Test case to verify the behavior of creating appointments with an incorrect appointment time format,
        specifically when the minute part of the appointment time is a single digit.

        This test performs the following steps:
        1. Finds the highest unique ID for appointments in the database.
        2. Retrieves the details of the latest doctor and patient.
        3. Modifies the current date-time to set the minute value to 5 for validation purposes.
        4. Constructs appointment data with the latest doctor and patient details and the modified appointment time.
        5. Sends a POST request to the appointments API endpoint with the constructed data.
        6. Asserts that the response status code is 400, indicating a bad request due to incorrect time format.
        7. Checks if the UID exists for the appointment created with the next unique ID.
        8. Asserts that the status code for UID existence check is not 200, indicating failure.

        This test ensures that the API rejects appointments with an incorrect time format,
        particularly when the minute part is a single digit.

        :param self: Instance of the test case class.
        :return: None
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()
        # Modify the minutes value in current date to validate
        current_dateTime  = current_dateTime.replace(minute=5)

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%m-%-dT%H:%-M"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200
    
    # Test case for creating a new appointment with wrong 24 hour time format
    def test_appointments_create_api_with_wrong_appointment_invalid_24_hour_format(self):
        """
        Test case to verify the behavior of creating appointments with an invalid appointment time format,
        specifically when using a 24-hour format with AM/PM indicators.

        This test performs the following steps:
        1. Finds the highest unique ID for appointments in the database.
        2. Retrieves the details of the latest doctor and patient.
        3. Modifies the current date-time to set the hour value to 16 for validation purposes.
        4. Constructs appointment data with the latest doctor and patient details and the modified appointment time.
        5. Sends a POST request to the appointments API endpoint with the constructed data.
        6. Asserts that the response status code is 400, indicating a bad request due to incorrect time format.
        7. Checks if the UID exists for the appointment created with the next unique ID.
        8. Asserts that the status code for UID existence check is not 200, indicating failure.

        This test ensures that the API rejects appointments with an invalid time format,
        particularly when using a 24-hour format with AM/PM indicators.

        :param self: Instance of the test case class.
        :return: None
        """
        
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, latest_patient_value = list(
            TestMedicalDB.list_of_patients.items()
        )[-1]

        current_dateTime = datetime.now()
        # Modify the time to 24 hour in order to validate
        current_dateTime  = current_dateTime.replace(hour=16)

        data = {
            "doctor_uid": latest_doctor_uid,
            "patient_uid": latest_patient_uid,
            "start_time": current_dateTime.strftime("%Y-%m-%-dT%I:%M %p"),
        }

        response = requests.post(
            f"{TestMedicalDB.base_url}/appointments",
            json=data,
            auth=latest_doctor_value,
        )
        assert response.status_code == 400

        status_code = check_if_uid_exists("appointments", max_unique_id + 1)
        assert status_code != 200

    # Test case for creating a new appointment with wrong date time without T separator format
    def test_appointments_create_api_with_wrong_appointment_without_T_separator_format(self):
        """
        Test case to verify the behavior of creating appointments with an invalid appointment time format,
        specifically when the time format does not include the 'T' separator between date and time.

        This test performs the following steps:
        1. Finds the highest unique ID for appointments in the database.
        2. Retrieves the details of the latest doctor and patient.
        3. Retrieves the current date-time.
        4. Constructs appointment data with the latest doctor and patient details and the current date-time without the 'T' separator.
        5. Sends a POST request to the appointments API endpoint with the constructed data.
        6. Asserts that the response status code is 400, indicating a bad request due to incorrect time format.
        7. Checks if the UID exists for the appointment created with the next unique ID.
        8. Asserts that the status code for UID existence check is not 200, indicating failure.

        This test ensures that the API rejects appointments with an invalid time format,
        particularly when the 'T' separator between date and time is missing.

        :param self: Instance of the test case class.
        :return: None
        """
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
            "start_time": current_dateTime.strftime("%Y-%m-%d %H:%M"),
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
        """Test creating a new appointment profile with a 30-minute time gap.

        This method tests the functionality of creating a new appointment profile with a
        30-minute time gap. It performs the following steps:

          1. Determines the highest UID currently existing in the "appointments" database table.
          2. Retrieves the UID and authentication value of the latest doctor and patient in the database.
          3. Retrieves the current date and time.
          4. Constructs data for the appointment creation with the doctor UID, patient UID, and the
             current date and time.
          5. Sends a POST request to create the appointment with the constructed data, authenticated
             with the doctor's credentials.
          6. Asserts that the response status code is 200.
          7. Checks if the UID of the newly created appointment exists in the "appointments" table.
          8. Adds the newly created appointment to the list of appointments.
          9. Calculates a new date and time by adding 30 minutes to the current date and time.
          10. Constructs data for creating a second appointment with the same doctor UID, patient UID,
              and the new date and time.
          11. Sends a POST request to create the second appointment with the constructed data,
              authenticated with the doctor's credentials.
          12. Asserts that the response status code is 200.
          13. Checks if the UID of the second appointment exists in the "appointments" table.
          14. Adds the second appointment to the list of appointments.

        Raises:
            AssertionError: If any of the assertions fail.
        """
        max_unique_id = self._find_highest_uid("appointments")

        latest_doctor_uid, latest_doctor_value = list(
            TestMedicalDB.list_of_doctors.items()
        )[-1]
        latest_patient_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

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

        TestMedicalDB.list_of_appointments[max_unique_id + 1] = (
            latest_doctor_uid,
            latest_patient_uid,
        )

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

        TestMedicalDB.list_of_appointments[max_unique_id + 2] = (
            latest_doctor_uid,
            latest_patient_uid,
        )

    def test_appointments_deletion_by_doctor(self):
        """Test deleting appointments by doctor.

        This method tests the functionality of deleting appointments by a doctor. It performs the following steps:

          1. Creates a doctor with the name "Dr. Higgs" and credentials "higgsbosn", "radiation", and "Boson".
          2. Retrieves the UID and authentication value of the created doctor.
          3. Creates a patient named "Mr. Electron" with credentials "electronenergy",
             "Electron123", "333444555666", and "electron@higgs.com".
          4. Retrieves the UID of the created patient.
          5. Creates an appointment for the created doctor and patient.
          6. Retrieves the UID of the latest appointment created.
          7. Deletes the appointment using the doctor's credentials.
          8. Asserts that the response status code is 200.
          9. Removes the appointment from the list of appointments.
          10. Checks if the appointment UID still exists in the database.

        Raises:
           AssertionError: If any of the assertions fail.
        """
        # Create the doctor
        self._util_doctor_create("Dr. Higgs ", "higgsbosn", "radiation", "Boson")
        doctor_uid, doctor_value = list(TestMedicalDB.list_of_doctors.items())[-1]

        # Create the patient parrot
        self._util_patients_create(
            "Mr. Electron",
            "electronenergy",
            "Electron123",
            "333444555666",
            "electron@higgs.com",
        )
        electron_uid, _ = list(TestMedicalDB.list_of_patients.items())[-1]

        # Create appointment for doctor and patient parrot
        self._util_appointments_create(
            doctor_uid,
            electron_uid,
            "electronenergy",
            "Electron123",
            generate_appointment_time(),
        )

        latest_appointment_uid, _ = list(TestMedicalDB.list_of_appointments.items())[-1]

        # Fetch the appointment details using patient parrot
        response = requests.delete(
            f"{TestMedicalDB.base_url}/appointments/{latest_appointment_uid}",
            auth=doctor_value,
        )

        assert response.status_code == 200
        del TestMedicalDB.list_of_appointments[latest_appointment_uid]

        status_code = check_if_uid_exists("appointments", latest_appointment_uid)

        assert status_code != 200

    # Test case for delete an new appointment by doctor
    def test_appointments_delete_by_patient_cred(self):
        """Test deleting appointments by patient credentials.

        This method tests the functionality of deleting appointments using patient credentials.
        It performs the following steps:

          1. Creates a doctor with the name "Dr. DoLittle2" and credentials "dolittle2", "veteneray", and "DoLittle123".
          2. Retrieves the UID of the created doctor.
          3. Creates a patient named "Bumble Bee1" with credentials "bumble1", "bumble123", "1234567", and
             "bumble@xyz.com".
          4. Retrieves the UID and authentication value of the created patient.
          5. Creates an appointment for the created doctor and patient.
          6. Fetches appointment details using the patient's credentials.
          7. Asserts that the received doctor UID matches the originally created doctor UID.
          8. Asserts that the received patient UID matches the originally created patient UID.
          9. Asserts that a non-zero appointment UID is received.
          10. Sends a DELETE request to delete the fetched appointment, authenticated with the patient's credentials.
          11. Asserts that the response status code is 200.
          12. Checks if the appointment UID still exists in the database.

        Raises:
            AssertionError: If any of the assertions fail.
        """

        # Create the doctor
        self._util_doctor_create(
            "Dr. DoLittle2 ", "dolittle2", "veteneray", "DoLittle123"
        )

        doctor_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

        # Create the patient 1
        self._util_patients_create(
            "Bumble Bee1", "bumble1", "bumble123", "1234567", "bumble@xyz.com"
        )
        patient1_uid, patient1_value = list(TestMedicalDB.list_of_patients.items())[-1]

        # Create appointment for doctor and patient 1
        self._util_appointments_create(
            doctor_uid,
            patient1_uid,
            "bumble1",
            "bumble123",
            generate_appointment_time(),
        )

        # Fetch the appointment details using patient 1
        response = requests.get(
            f"{TestMedicalDB.base_url}/appointments", auth=patient1_value
        )
        (
            recvd_doctor_uid,
            recvd_patient_uid,
            recvd_appointment_uid,
        ) = get_appointment_details(response.text)

        assert recvd_doctor_uid == doctor_uid
        assert recvd_patient_uid == patient1_uid
        assert recvd_appointment_uid != 0

        response = requests.delete(
            f"{TestMedicalDB.base_url}/appointments/{recvd_appointment_uid}",
            auth=patient1_value,
        )
        assert response.status_code == 200

        status_code = check_if_uid_exists("appointments", recvd_appointment_uid)

        assert status_code != 200

    # Test case for Modifying unique id of the doctor
    def test_unique_uids_cannot_be_modified(self):
        """
        Test case to verify the functionality of creating a new doctor through the API.

        This test performs the following steps:
            1. Finds the highest unique ID currently assigned to doctors in the database.
            2. Constructs data for creating a new doctor including full name, username,
               speciality, and password.
            3. Sends a POST request to the '/doctors' endpoint with the constructed data
               and admin authentication.
            4. Verifies that the response status code is 200 (OK).
            5. Checks if the newly created doctor's unique ID exists in the database.
            6. Adds the newly created doctor to the preconfigured list of doctors.
            7. Retrieves the list of unique IDs for doctors from the database and compares
               it with the updated list of preconfigured doctors.

        Returns:
            None: This test does not return anything. It asserts conditions
                  to ensure the correctness of the functionality being tested.
        """
        # Create a doctor
        self._util_doctor_create("Dr. Hulk", "unique_hulk", "gaestro", "hulk123")
        doctor_uid, _ = list(TestMedicalDB.list_of_doctors.items())[-1]

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
