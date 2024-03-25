import pytest
import requests
import logging
import json

class TestMedicalDB:
    # Basic initialization for prelimernay test
    admin_auth =  ("admin", "password")
    doctor_auth = ("paediatricianjohndoe", "DrJohnDoe")
    patient_auth = ("clientjanedoe", "JaneDoe")
    base_url = "http://medical_db:5000"

    # Find the highest uuid among the dataset
    def _find_highest_uuid(self, dataset):
        response = requests.get(f"{TestMedicalDB.base_url}/{dataset}", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
        response_dict = json.loads(response.text)
        unique_ids = set(entry["unique_id"] for entry in response_dict if "unique_id" in entry)

        max_unique_id = max(unique_ids)
        return max_unique_id 

    def test_get_doctors(self):
        response = requests.get(f"{TestMedicalDB.base_url}/doctors", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

    # Test case for retrieving a specific doctor's information
    def test_get_doctor_by_id(self):
        response = requests.get(f"{TestMedicalDB.base_url}/doctors/1", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200

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

        response = requests.get(f"{TestMedicalDB.base_url}/doctors/{max_unique_id}", auth=TestMedicalDB.admin_auth)
        assert response.status_code == 200
