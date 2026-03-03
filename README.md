# Lightweight WMS & CRM System

## What is this?
I built this desktop application to manage warehouse inventory and customer relationships (CRM). My main goal with this project was to translate business logic into Python code and design a solid, relational database structure from scratch. 

Instead of just building a simple CRUD app, I focused on data integrity and basic security practices.

## Tech Stack
* **Python 3**
* **SQLite3**
* **bcrypt**
* **CustomTkinter**
* **tktooltip**

## Under the Hood (Key Features)
* **Secure Logins:** Passwords are not stored in plain text. I used `bcrypt` to hash credentials, keeping basic security in mind.
* **Database Integrity:** The SQLite database uses `FOREIGN KEY` constraints and `ON DELETE CASCADE`. If a company is removed, all related warehouse orders are automatically cleared to prevent orphaned data.
* **Real-time Calculations:** SQL queries handle the math (total weights, order values, company-wide statistics) dynamically.

## What's Next? (DevOps Roadmap)
Since I am currently expanding my skills in DevOps and Cybersecurity, this desktop app is just phase one. My planned next steps for this repository are:

- [ ] **Docker:** Containerize the application so it can run anywhere without manual setup.
- [ ] **Database Migration:** Replace SQLite with a dedicated PostgreSQL server.
- [ ] **CI/CD:** Add GitHub Actions to automatically check the code quality on every commit.

## How to run it locally
1. Clone this repository to your machine.
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
