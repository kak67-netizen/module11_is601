
# Module 11: Calculation Model, Pydantic Validation, and CI/CD

## Overview

This project builds on the Module 10 FastAPI and PostgreSQL application by implementing a SQLAlchemy Calculation model, Pydantic validation schemas, an optional Factory design pattern, and automated tests.

The application also retains the secure User model, password hashing, PostgreSQL database integration, and Docker-based deployment from earlier modules.

GitHub Actions automatically runs unit, integration, and browser tests before building, scanning, and pushing the Docker image to Docker Hub.

## Technologies

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Playwright
- Docker and Docker Compose
- pgAdmin 4
- GitHub Actions
- Trivy security scanner
- pwdlib / Argon2

## Calculation Model

The SQLAlchemy Calculation model is defined in:

`app/models/calculation.py`

It contains the following fields:

| Field | Description |
|---|---|
| id | Primary key identifying each calculation |
| a | First numeric operand |
| b | Second numeric operand |
| type | Arithmetic operation |
| result | Calculated result |

The model maps to the PostgreSQL `calculations` table.

## Pydantic Calculation Schemas

The schemas are defined in:

`app/schemas/calculation.py`

### CalculationCreate

Validates incoming calculation data:

- `a`: First numeric operand
- `b`: Second numeric operand
- `type`: Arithmetic operation

Supported operations:

- Add
- Sub
- Multiply
- Divide

Validation rejects unsupported operation types and division by zero.

### CalculationRead

Defines the representation of a stored calculation, including its ID, operands, operation type, and result.

The schema supports reading data from SQLAlchemy model objects.

## Factory Design Pattern

The optional Factory pattern is implemented in:

`app/calculation_factory.py`

`CalculationFactory` selects the appropriate arithmetic function based on the requested operation.

The supported functions are defined in `app/operations.py`.

This keeps operation selection separate from database and validation logic.

## Existing User Authentication Features

The project retains the secure SQLAlchemy User model and Pydantic user schemas from Module 10.

Usernames and email addresses have unique constraints.

Passwords are hashed using Argon2 through `pwdlib`. Plain-text passwords are not stored in the database.

## Database Setup

PostgreSQL runs through Docker Compose.

Local development configuration:

- Database: `fastapi_db`
- Username: `postgres`
- Password: `postgres`
- Port: `5432`
- pgAdmin: `http://localhost:5050`

These credentials are intended for local development only.

Start the PostgreSQL database:

```bash
docker compose up -d db
```

Create a separate testing database if it does not already exist:

```bash
docker compose exec db psql -U postgres -d postgres -c "CREATE DATABASE fastapi_test_db;"
```

The test database should be kept separate from the application database because integration test fixtures create and remove database tables.

## Running Tests

Activate the project's virtual environment in Ubuntu WSL:

```bash
source .venv/bin/activate
```

Set the database connection for integration testing:

```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/fastapi_test_db"
```

Run Calculation unit tests:

```bash
python -m pytest tests/unit/test_calculation.py -v
```

Run Calculation integration tests:

```bash
python -m pytest tests/integration/test_calculation_database.py -v
```

Run all unit and integration tests:

```bash
python -m pytest tests/unit tests/integration -v
```

During local verification, 39 unit and integration tests passed.

## CI/CD Pipeline

The GitHub Actions workflow is defined in:

`.github/workflows/ci.yml`

The pipeline performs the following steps:

1. Starts a PostgreSQL service.
2. Installs Python dependencies.
3. Installs Chromium for Playwright.
4. Runs unit and integration tests.
5. Runs browser-based tests.
6. Authenticates with Docker Hub.
7. Builds the Docker image.
8. Scans the image for HIGH and CRITICAL vulnerabilities using Trivy.
9. Pushes the image to Docker Hub.

The Trivy scan reports detected vulnerabilities without automatically failing deployment.

## Docker Hub Deployment

Docker Hub repository:

https://hub.docker.com/r/keanek98/module11_is601

Pull the published image:

```bash
docker pull keanek98/module11_is601:latest
```

GitHub repository:

https://github.com/kak67-netizen/module11_is601

## Submission Evidence

The `screenshots` folder contains evidence of the successful GitHub Actions workflow and published Docker Hub image.

## Module 12 Scope

Calculation BREAD (Browse, Read, Edit, Add, Delete) API endpoints are not implemented in this module. They are reserved for Module 12.
