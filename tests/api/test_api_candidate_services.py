import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(autouse=True)
def clean_registry():
    requests.post(f"{BASE_URL}/reset")

@pytest.fixture
def sample_candidate():
    return {
        "first_name": "Jan",
        "last_name": "Testowy",
        "email": "jan@test.pl",
        "experience": 5,
        "salary_expectations": 15000
    }

def test_create_candidate_and_check_duplicate(sample_candidate):
    response = requests.post(f"{BASE_URL}/candidates", json=sample_candidate)
    assert response.status_code == 201
    assert response.json()['message'] == "Candidate created"
  
    check = requests.get(f"{BASE_URL}/candidates")
    assert len(check.json()) == 1

    # Sprawdzamy duplikat
    response = requests.post(f"{BASE_URL}/candidates", json=sample_candidate)
    assert response.status_code == 409
    assert response.json()['message'] == "Candidate with this email already exists"
    assert len(check.json()) == 1

def test_create_candidate_invalid_email():
    invalid_candidate = {
        "first_name": "Jan", "last_name": "Testowy",
        "email": "jan.test.pl",
        "experience": 5, "salary_expectations": 15000
    }
    response = requests.post(f"{BASE_URL}/candidates", json=invalid_candidate)
    assert response.status_code == 400
    
    check = requests.get(f"{BASE_URL}/candidates")
    assert len(check.json()) == 0

def test_get_all_candidates(sample_candidate):
    requests.post(f"{BASE_URL}/candidates", json=sample_candidate)
    
    response = requests.get(f"{BASE_URL}/candidates")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_update_candidate(sample_candidate):
    requests.post(f"{BASE_URL}/candidates", json=sample_candidate)

    update_data = {"first_name": "Piotr", "salary_expectations": 20000}
    response = requests.patch(f"{BASE_URL}/candidates/{sample_candidate['email']}", json=update_data)

    assert response.status_code == 200
    assert response.json()['message'] == "Candidate updated"

def test_delete_candidate(sample_candidate):
    requests.post(f"{BASE_URL}/candidates", json=sample_candidate)
    response = requests.delete(f"{BASE_URL}/candidates/{sample_candidate['email']}")
    assert response.status_code == 200
    assert response.json()['message'] == "Candidate deleted"
    check = requests.get(f"{BASE_URL}/candidates")
    assert len(check.json()) == 0