import pytest # pyright: ignore[reportMissingImports]
from src.candidate import Candidate
from src.job_offer import JobOffer
from src.application import Application

@pytest.fixture
def valid_candidate():
    return Candidate("Jan", "Kowalski", "jan@test.pl", 5, 10000.0)

@pytest.fixture
def valid_offer():
    return JobOffer("Senior Dev", 10000, 20000, 5)

@pytest.fixture
def application(valid_candidate, valid_offer):
    return Application(valid_candidate, valid_offer)

def test_create_valid_application(application):
    assert application.status == "NEW"
    assert application.rejection_reason is None

def test_create_application_salary_wrong(valid_offer):
    expensive_candidate = Candidate("Jan", "Bogaty", "jan@test.pl", 10, 50000.0)
    
    app = Application(expensive_candidate, valid_offer)
    
    assert app.status == "REJECTED"
    assert app.rejection_reason == "Salary expectations too high"

def test_create_application_experience_too_low(valid_offer):
    young_candidate = Candidate("Jan", "Mlody", "jan@test.pl", 3, 10000.0)

    app = Application(young_candidate, valid_offer)

    assert app.status == "REJECTED"
    assert app.rejection_reason == "Too little experience"

def test_create_application_invalid_candidate(valid_offer):
    invalid_candidate = Candidate("Jan", "Kowalski", "brak_malpy.pl", 5, 10000.0)
    
    app = Application(invalid_candidate, valid_offer)
    
    assert app.status == "REJECTED"
    assert app.rejection_reason == "Invalid candidate data"

def test_create_application_closed_offer(valid_candidate, valid_offer):
    valid_offer.close_offer() 
    
    app = Application(valid_candidate, valid_offer)
    
    assert app.status == "REJECTED"
    assert app.rejection_reason == "Offer is closed"
