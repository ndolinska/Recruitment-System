import pytest # pyright: ignore[reportMissingImports]
from pytest_mock import MockFixture
from src.candidate import Candidate

@pytest.fixture
def candidate(mocker: MockFixture):
    mocker.patch.object(Candidate, 'is_email_valid', return_value=True)
    return Candidate("Jan", "Kowalski", "jan@test.pl", 5, 10000.0)

def test_candidate_proper(candidate):
    assert candidate.first_name == "Jan"
    assert candidate.email == "jan@test.pl"

@pytest.mark.parametrize("offer_max_salary, expected_result", [
    (10000, True),  # Oferta równa oczekiwaniom -> OK
    (9000, True),   # Oferta niższa, ale mieści się w widełkach 20% (8333 to granica) -> OK
    (8000, False),  # Oferta za niska (10k > 8k + 20%) -> FAIL
    ("invalid", False) # Błędny typ danych -> FAIL
])
def test_salary_match_logic(candidate, offer_max_salary, expected_result):
    assert candidate.check_salary_match(offer_max_salary) is expected_result

def test_create_candidate_invalid_email(mocker: MockFixture, candidate):
    mocker.patch.object(Candidate, 'is_email_valid', return_value=False)
    c = Candidate("Jan", "Kowalski", "jan@test.pl", 5, 10000.0)
    assert c.email == "INVALID"
