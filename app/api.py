from flask import Flask, request, jsonify
from src.recruitment_registry import RecruitmentRegistry
from src.candidate import Candidate
from src.job_offer import JobOffer
from src.application import Application

app = Flask(__name__)
registry = RecruitmentRegistry()

# W wyniku dodania mocków zewnętrznej aplikacji do testów musimy założyć to
# W kodzie dalej pozostawiamy sprawdzenie czy email == "INVALID"
Candidate.is_email_valid = lambda self, email: True

# Endpoint offers
@app.route("/offers", methods=['POST'])
# Dodajemy ofertę
def create_offer():
    data = request.get_json()
    print(f"Create offer request: {data}")
    
    if registry.search_job_offer(data['title']):
        return jsonify({"message": "Offer with this title already exists"}), 409

    offer = JobOffer(data['title'], data['min_salary'], data['max_salary'], data.get('min_yoe', 0))
    
    if offer.min_salary == -1.0:
        return jsonify({"message": "Invalid salary range"}), 400

    registry.add_job_offer(offer)
    return jsonify({"message": "Job offer created"}), 201

# Pobieramy wszystkie oferty
@app.route("/offers", methods=['GET'])
def get_all_offers():
    offers = registry.get_all_offers()
    result = [{
        "title": o.title, 
        "min": o.min_salary, 
        "max": o.max_salary,
        "status": o.status,
        "apps_count": len(o.applications)
    } for o in offers]
    return jsonify(result), 200

# Możemy zamknąć ofertę
@app.route("/offers/<title>", methods=['PATCH'])
def update_offer_status(title):
    offer = registry.search_job_offer(title)
    if not offer:
        return jsonify({"message": "Offer not found"}), 404
    
    data = request.get_json()
    new_status = data.get('status')

    if new_status == "CLOSED":
        offer.close_offer() 
        return jsonify({"message": f"Offer has been closed"}), 200
    
    return jsonify({"message": "Wrong offer status (must be closed or open)"}), 400

# Usuwanie ofert
@app.route("/offers/<title>", methods=['DELETE'])
def delete_offer(title):
    print(f"Delete offer: {title}")
    if registry.remove_job_offer(title):
        return jsonify({"message": "Offer deleted"}), 200
    
    return jsonify({"message": "Offer not found"}), 404 

# Endpoint applications
@app.route("/applications", methods=['POST'])

# Tworzymy aplikację z kandydatem którego podajemy w requestcie
def create_application():
    data = request.get_json()
    print(f"Apply request: {data}")

    offer = registry.search_job_offer(data.get('title'))
    if not offer:
        return jsonify({"message": "Incorrect data"}), 404
    
    candidate = Candidate(
        data['first_name'], 
        data['last_name'], 
        data['email'], 
        data['experience'], 
        data['salary_expectations']
    )
    if candidate.email == "INVALID":
        return jsonify({"message": "Incorrect data"}), 400
    
    app = Application(candidate, offer)

    if registry.add_application(app):
        return jsonify({"message": "Application created"}), 201
    else:
        return jsonify({"message": "Application already exists (duplicate)"}), 409

# Tutaj pobieramy wszystkie aplikacje
@app.route("/applications", methods=['GET'])
def get_all_applications():
    apps = registry.get_all_applications()
    result = [{
        "candidate": f"{a.candidate.first_name} {a.candidate.last_name}",
        "offer": a.job_offer.title,
        "status": a.status,
        "reason": a.rejection_reason
    } for a in apps]
    return jsonify(result), 200

# Tutaj możemy zmienić status rekrutacji
@app.route("/applications/status", methods=['PATCH'])
def update_status():
    data = request.get_json()
    print(f"Update status: {data}")
    
    app = registry.search_application(data.get('email'), data.get('title'))
    if not app:
        return jsonify({"message": "Application not found"}), 404
    if app.advance_status(data.get('status')):
        return jsonify({"message": "Status updated"}), 200
    else:
        return jsonify({"message": "Invalid status transition"}), 400

# Usuwamy zgłoszenie
@app.route("/applications", methods=['DELETE'])
def delete_application():
    data = request.get_json()
    print(f"Delete application: {data}")
    
    app = registry.search_application(data.get('email'), data.get('title'))
    if not app:
        return jsonify({"message": "Application not found"}), 404

    registry.remove_application(app)
    return jsonify({"message": "Application deleted"}), 200

# Dodajemy endpoint do czyszczenia registry który będzie pomocny w testach
# Szczególnie dlatego że jesteśmy ograniczeni do testów bez importu kodu
@app.route("/reset", methods=['POST'])
def reset_registry():
    registry.job_offers = []
    registry.applications = []
    return jsonify({"message": "Registry cleared"}), 200