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

@pytest.fixture
def sample_offer():
    return {
        "title": "Python Developer",
        "min_salary": 10000,
        "max_salary": 20000
    }
@pytest.fixture
def sample_app(sample_candidate, sample_offer):
    return {
        "email": sample_candidate['email'],
        "title": sample_offer['title']
    }

@pytest.fixture
def ready_registry(client, sample_candidate, sample_offer):
    client.post("/candidates", json=sample_candidate)
    client.post("/offers", json=sample_offer)


def test_create_application_success_and_check_duplicate(client, sample_app, ready_registry):
    response = client.post("/applications", json=sample_app)
    
    assert response.status_code == 201
    assert response.json['message'] == "Application created"
    assert len(registry.applications) == 1

    try2 = client.post("/applications", json=sample_app)
    assert try2.status_code == 409
    assert try2.json['message'] == "Application already exists (duplicate)"

def test_create_application_missing_data(client):
    app_data = {"email": "duch@test.pl", "title": "Nieistnieje"}
    response = client.post("/applications", json=app_data)
    assert response.status_code == 404
    assert response.json['message'] == "Incorrect data"

# Tutaj wyjaśnienia bo to najcięższa część
def test_update_application_status(client, sample_candidate, sample_offer, sample_app, ready_registry):
    client.post("/applications", json=sample_app)
    # Update statusu na INTERVIEW
    update_data = {
        "email": sample_candidate['email'], 
        "title": sample_offer['title'],
        "status": "INTERVIEW"
    }
    response = client.patch("/applications/status", json=update_data)
    assert response.status_code == 200
    assert response.json['message'] == "Status updated"

    # Sprawdzenie czy status faktycznie się zmienił
    get_response = client.get("/applications")
    assert get_response.json[0]['status'] == "INTERVIEW"

    # Teraz sprawdzamy niedozwolone przejście
    update_data["status"] = "NEW"
    response = client.patch("/applications/status", json=update_data)
    assert response.status_code == 400
    assert response.json['message'] == "Invalid status transition"

    # Tutaj sprawdzamy co jak nie znajdzie konta (np. przez błędne dane w nowym jsonie)
    response = client.patch("/applications/status", json={})
    assert response.status_code == 404
    assert response.json['message'] == "Application not found"

def test_delete_application(client, sample_app, ready_registry):
    client.post("/applications", json=sample_app)

    response = client.delete("/applications", json={})

    assert response.status_code == 404
    assert response.json['message'] == "Application not found"

    response = client.delete("/applications", json=sample_app)

    assert response.status_code == 200
    assert response.json['message'] == "Application deleted"
    assert len(registry.applications) == 0
