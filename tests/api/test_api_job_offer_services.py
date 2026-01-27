import pytest
from app.api import app, registry

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def clean_registry():
    registry.candidates = []
    registry.job_offers = []
    registry.applications = []

@pytest.fixture
def sample_offer():
    return {
        "title": "Python Developer",
        "min_salary": 10000,
        "max_salary": 20000
    }
def test_create_offer_and_check_duplicate(client, sample_offer):
    response = client.post("/api/offers", json=sample_offer)
    assert response.status_code == 201
    assert response.json['message'] == "Job offer created"
    assert len(registry.job_offers) == 1
    try2 = client.post("/api/offers", json=sample_offer)
    assert try2.status_code == 409
    assert try2.json['message'] == "Offer with this title already exists"

def test_create_invalid_offer(client):
    invalid_offer = {
        "title": "Python Developer",
        "min_salary": 30000,
        "max_salary": 20000
    }
    response = client.post("/api/offers", json=invalid_offer)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid salary range"

def test_get_all_offers(client, sample_offer):
    client.post("/api/offers", json=sample_offer)
    response = client.get("/api/offers")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == sample_offer['title']

def test_delete_offer(client, sample_offer):
    client.post("/api/offers", json=sample_offer)
    response = client.delete(f"/api/offers/{sample_offer['title']}")
    assert response.status_code == 200
    assert response.json['message'] == "Offer deleted"

def test_delete_offer_nonexistant(client):
    response = client.delete("/api/offers/Janitor")
    assert response.status_code == 404
    assert response.json['message'] == "Offer not found"