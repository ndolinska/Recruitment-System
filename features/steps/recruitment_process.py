import requests
from behave import * 

URL = "http://localhost:5000"

@given('System is empty')
def step_reset_system(context):
    response = requests.post(f"{URL}/reset")
    assert response.status_code == 200

@step('I create a job offer with title: "{title}", min_salary: "{min_s}", max_salary: "{max_s}"')
def create_job_offer(context, title, min_s, max_s):
    json_body = {
        "title": title,
        "min_salary": int(min_s),
        "max_salary": int(max_s),
        "min_yoe": 2 
    }
    response = requests.post(URL + "/offers", json=json_body)
    assert response.status_code == 201

@step('I create an application for offer: "{title}", candidate: "{first}" "{last}", email: "{email}", expected salary: "{salary}"')
def create_application(context, title, first, last, email, salary):
    json_body = {
        "first_name": first,
        "last_name": last,
        "email": email,
        "experience": 5,
        "salary_expectations": int(salary),
        "title": title
    }
    response = requests.post(URL + "/applications", json=json_body)
    assert response.status_code == 201

@step('I update status of application for "{email}" in offer "{title}" to "{status}"')
def update_application_status(context, email, title, status):
    json_body = {
        "email": email,
        "title": title,
        "status": status
    }
    response = requests.patch(URL + "/applications/status", json=json_body)
    assert response.status_code == 200

@step('Job offer "{title}" exists in System')
def check_offer_exists(context, title):
    response = requests.get(URL + "/offers")
    assert response.status_code == 200
    offers = response.json()

    offer_titles = [o['title'] for o in offers]
    assert title in offer_titles, f"Offer {title} not found in {offer_titles}"

@step('Application for email "{email}" and offer "{title}" exists in System')
def check_application_exists(context, email, title):
    response = requests.get(URL + "/applications")
    assert response.status_code == 200
    apps = response.json()

    matching = [a for a in apps if a['offer'] == title]
    assert len(matching) > 0, f"No applications found for offer {title}"

@step('Application for email "{email}" and offer "{title}" has status "{status}"')
def check_application_status(context, email, title, status):
    response = requests.get(URL + "/applications")
    assert response.status_code == 200
    apps = response.json()
    
    found = False
    for app in apps:
        if app['offer'] == title and app['status'] == status:
            found = True
            break
            
    assert found, f"Application for {title} with status {status} not found. Apps: {apps}"

@step('I cannot update status of application for "{email}" in offer "{title}" to "{status}"')
def check_cannot_update_status(context, email, title, status):
    json_body = {
        "email": email,
        "title": title,
        "status": status
    }
    response = requests.patch(URL + "/applications/status", json=json_body)
    assert response.status_code == 400