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
def sample_candidate():
    return {
        "first_name": "Jan",
        "last_name": "Testowy",
        "email": "jan@test.pl",
        "experience": 5,
        "salary_expectations": 15000
    }

def test_create_candidate_and_check_duplicate(client, sample_candidate):
    response = client.post("/api/candidates", json=sample_candidate)
    assert response.status_code == 201
    assert response.json['message'] == "Candidate created"
    assert len(registry.candidates) == 1
    try2 = client.post("/api/candidates", json=sample_candidate)
    assert try2.status_code == 409
    assert try2.json['message'] == "Candidate with this email already exists"

def test_create_candidate_invalid_email(client):
    invalid_candidate = {
        "first_name": "Jan",
        "last_name": "Testowy",
        "email": "jan.test.pl",
        "experience": 5,
        "salary_expectations": 15000
    }
    response = client.post("/api/candidates", json=invalid_candidate)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid candidate data"
    assert len(registry.candidates) == 0
    
def test_get_all_candidates(client, sample_candidate):
    client.post("/api/candidates", json=sample_candidate)
    response = client.get("/api/candidates")
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['email'] == sample_candidate['email']

def test_update_candidate(client, sample_candidate):
    client.post("/api/candidates", json=sample_candidate)
    update_data = {
        "first_name": "Piotr",
        "last_name": "Andrzejewski",
        "salary_expectations": 20000,
        "experience": 10
    }
    response = client.patch(f"/api/candidates/{sample_candidate['email']}", json=update_data)
    
    assert response.status_code == 200
    assert response.json['message'] == "Candidate updated"

    response = client.patch(f"/api/candidates/ghost@email.com", json=update_data)
    assert response.status_code == 404
    assert response.json['message'] == "Candidate not found"
    

def test_delete_candidate(client, sample_candidate):
    client.post("/api/candidates", json=sample_candidate)
    response = client.delete(f"/api/candidates/{sample_candidate['email']}")
    assert response.status_code == 200
    assert response.json['message'] == "Candidate deleted"
    assert len(registry.candidates) == 0

def test_delete_candidate_nonexistant(client):
    response = client.delete("/api/candidates/ghost@test.pl")
    assert response.status_code == 404
    assert response.json['message'] == "Candidate not found"
