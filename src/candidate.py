# src/candidate.py
import requests
class Candidate:
    def __init__(self, first_name, last_name, email, experience, salary_expectations):
        self.first_name = first_name
        self.last_name = last_name

        # Walidacja emaila 
        if self.is_email_valid(email):
            self.email = email
        else:
            self.email = "INVALID"
    
        self.experience = experience
        self.salary_expectations = float(salary_expectations)

    def is_email_valid(self, email):
        # Walidacja poprzez mockowanie zewnętrznego API
        base_url = "https://api.email-verifier.io/v1/"
        endpoint = f"{base_url}verify?email={email}"
        try:
            response = requests.get(endpoint)
            data = response.json()
            return data.get("status") == "deliverable"
        except requests.RequestException as e:
            print(f"External Email API Connection Error: {e}")
            return False

    # Sprawdzenie czy kandydat mieści się w budżecie
    def check_salary_match(self, max_offer_salary):
        # Walidacja
        if not isinstance(max_offer_salary, (float, int)):
            return False
        # Jeśli chce więcej niż 20% ponad budżet - odrzucamy go
        return self.salary_expectations <= (max_offer_salary * 1.2)