# src/candidate.py

class Candidate:
    def __init__(self, first_name, last_name, email, experience, salary_expectations):
        self.first_name = first_name
        self.last_name = last_name

        # Walidacja emaila 
        self.email = email if self.is_email_valid(email) else "INVALID"
    
        self.experience = experience
        self.salary_expectations = float(salary_expectations)

    def is_email_valid(self, email):
        # Prosta walidacja: musi być stringiem, mieć @ i kropkę
        return isinstance(email, str) and "@" in email and "." in email

    # Sprawdzenie czy kandydat mieści się w budżecie
    def check_salary_match(self, max_offer_salary):
        # Walidacja
        if not isinstance(max_offer_salary, (float, int)):
            return False
        # Jeśli chce więcej niż 20% ponad budżet - odrzucamy go
        return self.salary_expectations <= (max_offer_salary * 1.2)