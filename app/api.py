from flask import Flask, request, jsonify
from src.recruitment_registry import RecruitmentRegistry
from src.candidate import Candidate
from src.job_offer import JobOffer
from src.application import Application

app = Flask(__name__)
registry = RecruitmentRegistry()

# Endpoint candidates
@app.route("/candidates", methods=['POST'])
# Tworzenie kandydata
def create_candidate():
    data = request.get_json()
    print(f"Create candidate request: {data}")
    if registry.search_candidate(data['email']):
        return jsonify({"message": "Candidate with this email already exists"}), 409
    
    candidate = Candidate(
        data['first_name'], data['last_name'], data['email'], 
        data['experience'], data['salary_expectations'])

    if candidate.email == "INVALID":
        return jsonify({"message": "Invalid candidate data"}), 400
    registry.add_candidate(candidate)
    return jsonify({"message": "Candidate created"}), 201

@app.route("/candidates", methods=['GET'])
# Pobieramy wszystkich kandydatów
def get_all_candidates():
    candidates = registry.get_all_candidates()
    result = [{
        "first_name": c.first_name, 
        "last_name": c.last_name, 
        "email": c.email,
        "experience": c.experience,
        "salary expectations": c.salary_expectations
    } for c in candidates]
    return jsonify(result), 200

# Dodajemy możliwość zmiany informacji kandydata (oprócz maila skoro jest naszym kluczem)
@app.route("/candidates/<email>", methods=['PATCH'])
def update_candidate(email):
    print(f"Update candidate request: {email}")
    data = request.get_json()

    candidate = registry.search_candidate(email)
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404

    if 'first_name' in data:
        candidate.first_name = data['first_name']
    if 'last_name' in data:
        candidate.last_name = data['last_name']
    if 'experience' in data:
        candidate.experience = data['experience']
    if 'salary_expectations' in data:
        candidate.salary_expectations = data['salary_expectations']
        
    return jsonify({"message": "Candidate updated"}), 200

@app.route("/candidates/<email>", methods=['DELETE'])
# Wyszukujemy kandydata przez email i usuwamy go
def delete_candidate(email):
    print(f"Delete candidate: {email}")
    candidate = registry.search_candidate(email)
    if not candidate:
        return jsonify({"message": "Candidate not found"}), 404
    registry.candidates.remove(candidate)
    return jsonify({"message": "Candidate deleted"}), 200

# Endpoint offers
@app.route("/offers", methods=['POST'])
# Dodajemy ofertę
def create_offer():
    data = request.get_json()
    print(f"Create offer request: {data}")
    
    if registry.search_job_offer(data['title']):
        return jsonify({"message": "Offer with this title already exists"}), 409

    offer = JobOffer(data['title'], data['min_salary'], data['max_salary'])
    
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

# Szukamy jednej konkretnej oferty przez tytuł
@app.route("/offers/<title>", methods=['DELETE'])
def delete_offer(title):
    print(f"Delete offer: {title}")
    offer = registry.search_job_offer(title)
    if not offer:
        return jsonify({"message": "Offer not found"}), 404
    registry.job_offers.remove(offer)
    return jsonify({"message": "Offer deleted"}), 200

# Endpoint applications
@app.route("/applications", methods=['POST'])

# Tworzymy aplikację podając maila i tytuł stanowiska
def create_application():
    data = request.get_json()
    print(f"Apply request: {data}")
    
    email = data.get('email')
    title = data.get('title')

    candidate = registry.search_candidate(email)
    offer = registry.search_job_offer(title)

    if not candidate or not offer:
        return jsonify({"message": "Incorrect data"}), 404
    
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
    registry.candidates = []
    registry.job_offers = []
    registry.applications = []
    return jsonify({"message": "Registry cleared"}), 200