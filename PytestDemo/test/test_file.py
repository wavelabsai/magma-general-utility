import pytest
import requests

BASE_URL = 'http://medical_db:5000'  # Update this with the appropriate URL of your running server


@pytest.fixture
def auth():
    return ("admin", "password")


def test_get_doctors(auth):
    response = requests.get(f"{BASE_URL}/doctors/", auth=auth)
    assert response.status_code == 200
    # You can add more assertions based on the response content


def test_get_doctor_by_id(auth):
    response = requests.get(f"{BASE_URL}/doctors/1", auth=auth)
    assert response.status_code == 200
    # You can add more assertions based on the response content


def test_get_nonexistent_doctor(auth):
    response = requests.get(f"{BASE_URL}/doctors/100", auth=auth)
    assert response.status_code == 400
    # You can add more assertions based on the response content


# Similarly, you can write tests for other endpoints (Patients, Appointments) in a similar fashion
