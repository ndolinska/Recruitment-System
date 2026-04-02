# System Zarządzania Rekrutacją (Recruitment Management System)
### Opis projektu
* **Funkcjonalności:**
    1.  Walidacja widełek płacowych w ofertach (min < max).
    2.  Sprawdzanie dopasowania finansowego kandydata (limit +20% budżetu).
    3.  Weryfikacja minimalnego doświadczenia (YoE) względem wymagań oferty.
    4.  Blokowanie nielogicznych przejść aplikacji, np. z HIRED do REJECTED.
    5.  Automatyczne odrzucanie nieprzyjętych kandydatów przy zamykaniu oferty.
    6.  Blokowanie duplikatów aplikacji tego samego kandydata na tę samą ofertę.
* **3 współpracujące klasy:** `Candidate`, `JobOffer`, `Application`.
* **Rejestr danych:** Klasa `RecruitmentRegistry` przechowująca historię ofert i zgłoszeń.
* **Funkcjonalność zewnętrzna (Mockowana):** Weryfikacja adresu email kandydata za pomocą zewnętrznego API (email-verifier.io).
* **Pełen CRUD API:** Obsługa żądań POST, GET, PATCH, DELETE dla ofert i aplikacji.
### Testy
* **Unit:** `pytest` + `pytest-mock` (Pokrycie >80%)
* **API:** `requests` (Testy typu "czarna skrzynka" - brak importu kodu aplikacji)
* **BDD:** `behave` (Scenariusze Gherkin)
* **Performance:** `pytest` + `requests` (Pomiar czasu reakcji poniżej 0.5s przy 100 operacjach)

*Każdy rodzaj testów posiada oddzielny pipeline automatycznie uruchamiany przy push lub pull request.*

### Instrukcja uruchomienia i testowania
* Sklonuj repozytorium
* Zainstaluj requirements
`pip install -r requirements.txt`
* Uruchom flaska
`python -m flask --app app/api.py --debug run`
* Uruchom testy w oddzielnym terminalu
`python -m pytest tests`
* Uruchom testy BDD
`behave`

# ENG:
# Recruitment Management System
## Project Description
* **Features:**
  1. Validation of salary ranges in job offers (min < max).
  2. Candidate financial fit check (up to +20% of the budget allowed).
  3. Verification of minimum experience (YoE) against job requirements.
  4. Prevention of invalid application state transitions (e.g., from HIRED to REJECTED).
  5. Automatic rejection of pending candidates when a job offer is closed.
  6. Prevention of duplicate applications from the same candidate for the same job offer.

* **Core Classes:** `Candidate`, `JobOffer`, `Application`

* **Data Registry:** `RecruitmentRegistry` class storing the history of job offers and applications.

* **External Integration (Mocked):** Candidate email verification via an external API (email-verifier.io).

* **Full CRUD API:** Supports POST, GET, PATCH, DELETE operations for job offers and applications.

## Testing
* **Unit Tests:** `pytest` + `pytest-mock` (Coverage > 80%)
* **API Tests:** `requests` (black-box testing – no direct import of application code)
* **BDD Tests:** `behave` (Gherkin scenarios)
* **Performance Tests:** `pytest` + `requests` (response time under 0.5s for 100 operations)

*Each type of test has a separate pipeline automatically triggered on push or pull request.*

## Setup and Running
* Clone the repository
* Install dependencies:
  ```bash
  pip install -r requirements.txt
* Run the Flask app:
`python -m flask --app app/api.py --debug run`
* Run tests (in a separate terminal):
`python -m pytest tests`
* Run BDD tests:
`behave`
