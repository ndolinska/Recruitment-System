import pytest # pyright: ignore[reportMissingImports]
from src.job_offer import JobOffer

@pytest.fixture
def offer():
    return JobOffer("Senior Dev", 10000, 20000)

# Sprawdzamy czy konstruktor działa dobrze
def test_create_valid_offer(offer):
    assert offer.title == "Senior Dev"
    assert offer.min_salary == 10000.0
    assert offer.max_salary == 20000.0
    assert offer.status == "OPEN"
    assert offer.applications == []

@pytest.mark.parametrize("min_s, max_s", [
    (20000, 10000),   # Min > Max (Błąd logiczny)
    (-5000, 10000),   # Ujemne min
    (10000, -200),    # Ujemne max
    ("10k", 20000),   # Błędny typ
    (10000, None)     # None
])
def test_create_invalid_salary(min_s, max_s):
    offer = JobOffer("Tester", min_s, max_s)
    assert offer.min_salary == -1.0
    assert offer.max_salary == -1.0
    
# Sprawdzamy zmiane stanu
def test_close_offer(offer):
    offer.close_offer()
    assert offer.status == "CLOSED"

