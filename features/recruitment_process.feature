Feature: Recruitment Process
  Background: Clean Environment
    Given System is empty

  Scenario: Successfuly hiring a candidate
    When I create a job offer with title: "Senior Python Dev", min_salary: "15000", max_salary: "25000"
    Then Job offer "Senior Python Dev" exists in System

    When I create an application for offer: "Senior Python Dev", candidate: "Jan" "Kowalski", email: "jan@test.pl", expected salary: "20000"
    Then Application for email "jan@test.pl" and offer "Senior Python Dev" exists in System
    And Application for email "jan@test.pl" and offer "Senior Python Dev" has status "NEW"

    When I update status of application for "jan@test.pl" in offer "Senior Python Dev" to "INTERVIEW"
    Then Application for email "jan@test.pl" and offer "Senior Python Dev" has status "INTERVIEW"
    
    When I update status of application for "jan@test.pl" in offer "Senior Python Dev" to "HIRED"
    Then Application for email "jan@test.pl" and offer "Senior Python Dev" has status "HIRED"
    And I cannot update status of application for "jan@test.pl" in offer "Senior Python Dev" to "REJECTED"