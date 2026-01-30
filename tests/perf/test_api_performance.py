import pytest
import requests

url = "http://127.0.0.1:5000"
class TestPerf:
    def setup_method(self):
        requests.post(f"{url}/reset")
    # Testujemy szybkość postowania kandydatów
    def test_perf_create_application_loop(self):
        offer_data = {
            "title": "Performance Tester",
            "min_salary": 10000,
            "max_salary": 20000,
            "min_yoe": 1
        }
        resp = requests.post(f"{url}/offers", json=offer_data)
        assert resp.status_code == 201

        for i in range(100):
            candidate_data = {
                "first_name": "Szybki",
                "last_name": f"Kandydat_{i}",
                "email": f"fast_{i}@test.pl", 
                "experience": 2,
                "salary_expectations": 12000,
                "title": "Performance Tester"
            }
            
            try:
                response = requests.post(f"{url}/applications", json=candidate_data, timeout=0.5)
                assert response.status_code == 201
                
            except requests.exceptions.Timeout:
                pytest.fail(f"Performance check failed! Create Application took longer than 0.5s at iteration {i}")
        get_resp = requests.get(f"{url}/applications")
        assert get_resp.status_code == 200
        assert len(get_resp.json()) == 100, "System lost the applications"

    # Testujemy szybkość zmieniania statusów
    def test_perf_status_update_loop(self):
        offer_title = "Java Dev"
        requests.post(f"{url}/offers", json={"title": offer_title, "min_salary": 10, "max_salary": 20, "min_yoe": 0})
        
        candidates = []
        for i in range(50):
            email = f"update_{i}@test.pl"
            candidates.append(email)
            requests.post(f"{url}/applications", json={
                "first_name": "Jan", "last_name": "Test", "email": email,
                "experience": 2, "salary_expectations": 15, "title": offer_title
            })

        for i, email in enumerate(candidates):
            update_data = {
                "email": email,
                "title": offer_title,
                "status": "INTERVIEW"
            }
            try:
                resp = requests.patch(f"{url}/applications/status", json=update_data, timeout=0.5)
                assert resp.status_code == 200
                
            except requests.exceptions.Timeout:
                pytest.fail(f"Performance check failed! Status Update took longer than 0.5s at iteration {i}")

        get_resp = requests.get(f"{url}/applications")
        apps = get_resp.json()

        last_app = next((a for a in apps if a['email'] == candidates[-1]), None)
        assert last_app is not None
        assert last_app['status'] == "INTERVIEW", "Status was updated improperly"