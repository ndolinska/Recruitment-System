import pytest # pyright: ignore[reportMissingImports]
from src.candidate import Candidate
from src.job_offer import JobOffer
from src.application import Application

@pytest.fixture
def valid_candidate():
    return Candidate("Jan", "Kowalski", "jan@test.pl", 5, 10000.0)

@pytest.fixture
def valid_offer():
    return JobOffer("Senior Dev", 10000, 20000)

@pytest.fixture
def application(valid_candidate, valid_offer):
    return Application(valid_candidate, valid_offer)

@pytest.mark.parametrize("current_status, next_status, expected_success", [
    ("NEW", "INTERVIEW", True),      # Normalna ścieżka
    ("INTERVIEW", "HIRED", True),    # Sukces
    ("INTERVIEW", "REJECTED", True), # Odrzucenie po rozmowie
    ("NEW", "REJECTED", True),       # Odrzucenie na starcie
    ("NEW", "HIRED", False),         # Przeskok etapu (niedozwolone)
    ("REJECTED", "HIRED", False),    # Przywrócenie (niedozwolone)
    ("HIRED", "REJECTED", False)     # Zwolnienie (niedozwolone)
])
def test_status_transitions(application, current_status, next_status, expected_success):
    application.status = current_status
    
    result = application.advance_status(next_status)
    
    assert result is expected_success
    if expected_success:
        assert application.status == next_status
    else:
        # Stan nie powinien ulec zmianie
        assert application.status == current_status