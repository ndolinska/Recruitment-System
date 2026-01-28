from src.application import Application

class RecruitmentRegistry:
    def __init__(self):
        self.job_offers = []
        self.applications = []

    # Obsługa ofert pracy
    def add_job_offer(self, offer):
        if not self.search_job_offer(offer.title):
            self.job_offers.append(offer)
    
    def search_job_offer(self, title):
        for offer in self.job_offers:
            if offer.title == title:
                return offer
        return None
    
    def get_all_offers(self):
        return self.job_offers
    
    def remove_job_offer(self, title):
        offer = self.search_job_offer(title)
        if not offer or offer.status == ["OPEN"]:
            return False
        self.applications = [app for app in self.applications if app.job_offer.title != title]
        self.job_offers.remove(offer)
        return True
    
    # Obsługa aplikacji
    def add_application(self, app):
        if app.job_offer.add_application(app):
            self.applications.append(app)
            return True
        return False

    def search_application(self, email, title):
        for app in self.applications:
            if app.candidate.email == email and app.job_offer.title == title:
                return app
        return None
    
    def get_all_applications(self):
        return self.applications
    
    def remove_application(self, app):
        if app in self.applications:
            self.applications.remove(app)
        if app in app.job_offer.applications:
            app.job_offer.applications.remove(app)
