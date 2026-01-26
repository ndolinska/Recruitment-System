from src.application import Application

class RecruitmentRegistry:
    def __init__(self):
        self.candidates = []
        self.job_offers = []
        self.applications = []

    # Obsługa kandydatów
    def add_candidate(self, candidate):
        self.candidates.append(candidate)

    def search_candidate(self, email):
        for candidate in self.candidates:
            if candidate.email == email:
                return candidate
        return None
    
    def get_all_candidates(self):
        return self.candidates
    
    # Obsługa ofert pracy
    def add_job_offer(self, offer):
        self.job_offers.append(offer)
    
    def search_job_offer(self, title):
        for offer in self.job_offers:
            if offer.title == title:
                return offer
        return None
    
    def get_all_offers(self):
        return self.job_offers
    
    # Obsługa aplikacji
    def add_application(self, app):
        if app.job_offer.add_application(app):
            self.applications.append(app)

    def search_application(self, email, title):
        for app in self.applications:
            if app.candidate.email == email and app.job_offer.title == title:
                return app
        return None
    
    def get_applications_by_status(self, goal_status):
        res = []
        for app in self.applications:
            if app.status == goal_status:
                res.append(app)
        return res
    
    def remove_application(self, app):
        if app in self.applications:
            self.applications.remove(app)
        if app in app.job_offer.applications:
            app.job_offer.applications.remove(app)
