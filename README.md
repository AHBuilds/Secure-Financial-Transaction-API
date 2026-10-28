# Secure Financial Transaction API

A capstone project focused on developing a secure financial transaction API using **Python, FastAPI, and MySQL**. This project demonstrates authentication, authorization, password security, SQL injection prevention, and database-level transaction integrity controls.

## Features

- **JWT Authentication:** Uses JSON Web Tokens (JWT) to authenticate users accessing protected API endpoints.
- **Password Security:** Implements bcrypt-based password hashing to avoid storing plaintext passwords.
- **SQL Injection Prevention:** Uses parameterized SQL queries to handle user input safely.
- **Role-Based Access Control:** Organizes user permissions using application roles.
- **Database Integrity:** Uses MySQL stored procedures and transaction rollback handling to enforce business rules and prevent invalid transaction-state changes.
- **Security Testing:** Uses Burp Suite and SQLMap to test selected authentication, authorization, request-handling, and SQL injection scenarios.
- **Web Interface:** Includes an HTML, CSS, and JavaScript frontend connected to the backend API.

## Technology Stack

- **Programming Language:** Python
- **Backend Framework:** FastAPI
- **Database:** MySQL
- **Authentication:** JWT and HTTP Bearer authentication
- **Password Hashing:** Passlib and bcrypt
- **Frontend:** HTML, CSS, JavaScript, and Jinja2
- **Security Testing Tools:** Burp Suite and SQLMap
- **Development Tools:** MySQL Workbench and Uvicorn

- ## Security Implementation

The application incorporates several security controls:

- **Authentication and Authorization:** JWT-based authentication protects API endpoints that require a valid access token.
- **Credential Protection:** Passwords are hashed before storage using bcrypt-based password hashing.
- **Input Handling:** Parameterized SQL queries help prevent user input from being interpreted as executable SQL.
- **Transaction Validation:** Stored procedures enforce database-level business rules for transaction operations.
- **Rollback Handling:** Failed transaction operations can be rolled back to help preserve database consistency.

## Testing and Evaluation

Burp Suite and SQLMap were used to evaluate selected security scenarios, including authentication and authorization behavior, HTTP request manipulation, transaction-state validation, and SQL injection attempts.

The results and limitations of the tests performed are documented in the final project report.

## Documentation

The `report/` folder contains the final capstone report, which details the project's objectives, architecture, implementation, software tools, design decisions, challenges encountered, testing methodology, experimental results, and conclusions.

The `sql/` and `screenshots/` folders provide supporting database scripts and visual evidence of implementation and testing.

## Disclaimer

This project was developed for **educational and demonstration purposes**. The security testing performed covers selected scenarios and does not guarantee that the application is free of vulnerabilities. Further security review, testing, and production hardening would be necessary before using the application to process real financial transactions.

## Author

**Abraham H.**
