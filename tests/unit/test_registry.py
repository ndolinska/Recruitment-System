import pytest # pyright: ignore[reportMissingImports]
from pytest_mock import MockFixture
from src.recruitment_registry import RecruitmentRegistry
from src.candidate import Candidate
from src.job_offer import JobOffer
from src.application import Application

@pytest.fixture
def registry():
    return RecruitmentRegistry()

@pytest.fixture
def sample_candidate(mocker: MockFixture):
    mocker.patch.object(Candidate, 'is_email_valid', return_value=True)
    return Candidate("Jan", "Testowy", "jan@test.pl", 5, 12000)

@pytest.fixture
def sample_offer():
    return JobOffer("Senior Dev", 10000, 20000)

@pytest.fixture
def sample_application(sample_candidate, sample_offer):
    return Application(sample_candidate, sample_offer)

# Testy rejestru ofert
def test_add_and_search_offer(registry, sample_offer):
    registry.add_job_offer(sample_offer)
    
    assert len(registry.get_all_offers()) == 1
    
    found = registry.search_job_offer("Senior Dev")
    assert found == sample_offer

def test_search_offer_not_found(registry):
    result = registry.search_job_offer("Mid Dev")
    assert result is None

def test_delete_offer_and_application(registry, sample_offer, sample_application):
    registry.add_job_offer(sample_offer)
    assert len(registry.get_all_offers()) == 1
    registry.add_application(sample_application) 
    assert len(registry.get_all_applications()) == 1

    registry.remove_job_offer(sample_offer.title)
    assert len(registry.get_all_offers()) == 0
    assert len(registry.get_all_applications()) == 0
    assert registry.remove_job_offer(sample_offer.title) == False
    
# Testy rejestru zgłoszeń
def test_add_and_search_application(registry, sample_application):
    registry.add_application(sample_application)
    
    assert len(registry.applications) == 1
    
    found = registry.search_application("jan@test.pl", "Senior Dev")
    assert found == sample_application
    assert found.status == "NEW"

def test_reject_duplicate_applications(registry, sample_application):
    registry.add_application(sample_application)
    assert registry.add_application(sample_application) == False

def test_search_application_not_found(registry):
    result = registry.search_application("jan@test.pl", "DevOps")
    assert result is None

def test_remove_application(registry, sample_application):
    registry.add_application(sample_application)

    assert len(registry.get_all_applications()) == 1
    assert len(sample_application.job_offer.applications) == 1

    registry.remove_application(sample_application)

    assert len(registry.applications) == 0    
    assert len(sample_application.job_offer.applications) == 0 