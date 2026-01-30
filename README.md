# System Zarządzania Rekrutacją (Recruitment Management System)

**Autor:** Nadia Dolińska 

**Grupa:** 1  
  
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
