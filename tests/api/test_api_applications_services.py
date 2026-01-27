import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(autouse=True)
def clean_registry():
    requests.post(f"{BASE_URL}/reset")

@pytest.fixture
def sample_candidate():
    return {
        "first_name": "Jan", "last_name": "Testowy",
        "email": "jan@test.pl", "experience": 5, 
        "salary_expectations": 15000
    }

@pytest.fixture
def sample_offer():
    return {
        "title": "Python Developer",
        "min_salary": 10000, "max_salary": 20000
    }

@pytest.fixture
def sample_app(sample_candidate, sample_offer):
    return {
        "email": sample_candidate['email'],
        "title": sample_offer['title']
    }

@pytest.fixture
def ready_registry(sample_candidate, sample_offer):
    requests.post(f"{BASE_URL}/candidates", json=sample_candidate)
    requests.post(f"{BASE_URL}/offers", json=sample_offer)

def test_create_application_and_check_duplicate(sample_app, ready_registry):
    response = requests.post(f"{BASE_URL}/applications", json=sample_app)
    
    assert response.status_code == 201
    assert response.json()['message'] == "Application created"

    # Sprawdzenie duplikatu
    response = requests.post(f"{BASE_URL}/applications", json=sample_app)
    assert response.status_code == 409
    assert response.json()['message'] == "Application already exists (duplicate)"

def test_create_application_missing_data():
    app_data = {"email": "duch@test.pl", "title": "Nieistnieje"}
    
    response = requests.post(f"{BASE_URL}/applications", json=app_data)
    assert response.status_code == 404
    assert response.json()['message'] == "Incorrect data"

def test_get_all_applications(sample_app, ready_registry):
    requests.post(f"{BASE_URL}/applications", json=sample_app)
    response = requests.get(f"{BASE_URL}/applications")
    assert response.status_code == 200
    assert len(response.json()) == 1
    

def test_update_application_status(sample_app, ready_registry):
    requests.post(f"{BASE_URL}/applications", json=sample_app)
    update_data = {
        "email": sample_app['email'], 
        "title": sample_app['title'],
        "status": "INTERVIEW"
    }
    response = requests.patch(f"{BASE_URL}/applications/status", json=update_data)
    assert response.status_code == 200
    assert response.json()['message'] == "Status updated"

    get_res = requests.get(f"{BASE_URL}/applications")
    assert get_res.json()[0]['status'] == "INTERVIEW"

    # Sprawdzam przejście
    update_data["status"] = "NEW" # Cofanie się jest zabronione
    fail_res = requests.patch(f"{BASE_URL}/applications/status", json=update_data)
    assert fail_res.status_code == 400 
    assert "Invalid status" in fail_res.json()['message']

def test_delete_application(sample_app, ready_registry):
    requests.post(f"{BASE_URL}/applications", json=sample_app)

    response = requests.delete(f"{BASE_URL}/applications", json=sample_app)
    
    assert response.status_code == 200
    assert response.json()['message'] == "Application deleted"

    check = requests.get(f"{BASE_URL}/applications")
    assert len(check.json()) == 0