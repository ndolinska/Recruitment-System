class JobOffer:
    def __init__(self, title, min_salary, max_salary, min_yoe=0):
        self.title = title
        self.status = "OPEN"
        self.min_yoe = min_yoe 
        self.applications = []  # Lista aplikacji na tę ofertę.
        
        # Walidacja widełek płacowych
        if self.are_salaries_valid(min_salary, max_salary):
            self.min_salary = float(min_salary)
            self.max_salary = float(max_salary)
        else:
            self.min_salary = -1.0
            self.max_salary = -1.0

    # Metoda walidacji
    def are_salaries_valid(self, min_s, max_s):
        if not (isinstance(min_s, (int, float)) and isinstance(max_s, (int, float))):
            return False
        if min_s < 0 or max_s < 0:
            return False
        if min_s > max_s:
            return False
        return True
    
    # Zamykanie oferty
    def close_offer(self):
        self.status = "CLOSED"
        for app in self.applications:
            if app.status in ["NEW", "INTERVIEW"]:
                app.status = "REJECTED"
                app.rejection_reason = "Offer has been closed"

    def add_application(self, application):
        for existing_app in self.applications:
            if existing_app.candidate.email == application.candidate.email:
                return False
        
        self.applications.append(application)
        return True
