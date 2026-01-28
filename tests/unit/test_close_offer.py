import pytest
from src.job_offer import JobOffer
from src.application import Application
from src.candidate import Candidate
from pytest_mock import MockFixture

@pytest.fixture(autouse=True)
def mock_api_calls(mocker: MockFixture):
    mocker.patch.object(Candidate, 'is_email_valid', return_value=True)

@pytest.fixture
def offer():
    return JobOffer("Python Developer", 10000, 20000, min_yoe=2)

def test_close_offer_state_update_logic(offer):
    statuses = ["NEW", "INTERVIEW", "HIRED", "REJECTED"]
    
    for i, status in enumerate(statuses):
        c = Candidate("Jan", "Kowalski", f"jan{i}@test.pl", 5, 15000)
        app = Application(c, offer)
        app.status = status
        if status == "REJECTED":
            app.rejection_reason = "Old reason"
        offer.add_application(app)

    offer.close_offer()

    assert offer.applications[0].status == "REJECTED" # Był NEW
    assert offer.applications[1].status == "REJECTED" # Był INTERVIEW
    assert offer.applications[2].status == "HIRED"    # Był HIRED
    assert offer.applications[3].rejection_reason == "Old reason" # Był REJECTED
