class Application:
    def __init__(self, candidate, job_offer):
        self.candidate = candidate
        self.job_offer = job_offer
        self.status = "NEW"
        self.rejection_reason = None
        
        # Logika walidacji aplikacji, automatyczne stan "REJECTED" jeżeli nie
        # spełnione minimalne wymagania.
        self.validate_application()

    def validate_application(self):
        # Sprawdź czy email kandydata jest poprawny 
        if self.candidate.email == "INVALID":
            self.status = "REJECTED"
            self.rejection_reason = "Invalid candidate data"
            return

        # Sprawdź wymagania finansowe, korzystając z metody zdefiniowanej 
        # w klasie Candidate
        if not self.candidate.check_salary_match(self.job_offer.max_salary):
            self.status = "REJECTED"
            self.rejection_reason = "Salary expectations too high"
            return
        
        if self.job_offer.min_yoe > self.candidate.experience:
            self.status = "REJECTED"
            self.rejection_reason = "Too little experience"
            return

        # Jeśli oferta jest już zamknięta, też odrzucamy
        if self.job_offer.status != "OPEN":
            self.status = "REJECTED"
            self.rejection_reason = "Offer is closed"
            return

    # Metoda pozwalająca zmieniać etap rekrutacji, pilujemy też żeby działo 
    # się to w logiczny sposób.
    def advance_status(self, new_status):
        # Dozwolone przejścia
        allowed_transitions = {
            "NEW": ["INTERVIEW", "REJECTED"],   # Nową aplikację możemy odrzucić lub przenieść dalej
            "INTERVIEW": ["HIRED", "REJECTED"], # Po rozmowie kwalifikacyjnej możemy zatrudnić lub odrzucić
            "HIRED": [],    # Z zatrudnionego nie zmieniamy statusu
            "REJECTED": []  # Z odrzuconego nie można przywrócić
        }

        # Logika warunkowa sprawdzająca poprawność przejścia
        if new_status in allowed_transitions.get(self.status, []):
            self.status = new_status
            return True
        return False
    


   