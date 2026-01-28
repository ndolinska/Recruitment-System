import pytest
import requests

BASE_URL = "http://localhost:5000"

@pytest.fixture(autouse=True)
def clean_registry():
    requests.post(f"{BASE_URL}/reset")

@pytest.fixture
def sample_offer():
    return {
        "title": "Python Developer",
        "min_salary": 10000,
        "max_salary": 20000
    }

def test_create_offer_and_check_duplicate(sample_offer):
    response = requests.post(f"{BASE_URL}/offers", json=sample_offer)
    assert response.status_code == 201
    assert response.json()['message'] == "Job offer created"
    
    check = requests.get(f"{BASE_URL}/offers")
    assert len(check.json()) == 1
    
    # Duplikat
    response = requests.post(f"{BASE_URL}/offers", json=sample_offer)
    assert response.status_code == 409
    assert response.json()['message'] == "Offer with this title already exists"

def test_create_invalid_offer():
    invalid_offer = {
        "title": "Junior",
        "min_salary": 30000, 
        "max_salary": 20000 
    }
    response = requests.post(f"{BASE_URL}/offers", json=invalid_offer)
    assert response.status_code == 400
    assert response.json()['message'] == "Invalid salary range"

def test_get_all_offers(sample_offer):
    requests.post(f"{BASE_URL}/offers", json=sample_offer)
    
    response = requests.get(f"{BASE_URL}/offers")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_close_offer(sample_offer):
    requests.post(f"{BASE_URL}/offers", json=sample_offer)
    response = requests.patch(f"{BASE_URL}/offers/{sample_offer['title']}", json={"status": "CLOSED"})
    assert response.status_code == 200
    assert response.json()["message"] == "Offer has been closed"
    
    offers = requests.get(f"{BASE_URL}/offers").json()
    assert offers[0]["status"] == "CLOSED"

def test_delete_offer(sample_offer):
    requests.post(f"{BASE_URL}/offers", json=sample_offer)
    
    response = requests.delete(f"{BASE_URL}/offers/{sample_offer['title']}")
    assert response.status_code == 200
    assert response.json()['message'] == "Offer deleted"

