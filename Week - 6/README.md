# Week 6 – MLOps: Model Deployment with Lambda, MLflow, and Integration Tests

This project is a complete mini-pipeline for deploying and testing a machine learning model using AWS Lambda, MLflow, and Docker. It also incorporates infrastructure automation, code quality checks, unit and integration testing, and CI/CD-friendly tooling like `Makefile`.

---

## 🔧 Core Objectives

- Serve an ML model with **AWS Lambda**
- Track and retrieve model artifacts using **MLflow**
- Publish predictions to **Amazon Kinesis**
- Run **unit tests** and **integration tests**
- Use **Docker** for environment standardization
- Automate tasks using **Makefile**
- Apply **code quality and formatting tools**

---

## 📦 Folder Structure

Week - 6/
│
├── code/ ← Main codebase
│ ├── lambda_function.py ← AWS Lambda entry point
│ ├── model.py ← Prediction logic and model loading
│ ├── tests/ ← Unit tests
│ ├── integraton-test/ ← Integration testing with Docker
│ ├── scripts/ ← Deployment automation (ECR publishing)
│ ├── infrastructure/ ← Infra-as-code (not detailed here)
│ └── Makefile, Dockerfile ← Build, test, and serve automation
│
├── images/ ← (Ignore for this module)
├── meta.json, docs.md ← (Ignore for this module)
└── plan.md ← Summary of learning goals


---

## 🧪 Testing Strategy

| Type             | Location              | Tool        |
|------------------|-----------------------|-------------|
| Unit Tests       | `code/tests/`         | `pytest`    |
| Integration Test | `code/integraton-test/` | Docker Compose + Python |
| Cloud Simulation | `LocalStack` (in `run.sh`) | AWS mocks  |

---

## 📋 Setup Instructions

```bash
make setup        # Install dependencies & pre-commit hooks
make quality_checks  # Run black, isort, pylint
make test         # Run unit tests
make build        # Build Docker image
make integration_test  # Run integration test via docker-compose
make publish      # (Simulated) Publish image to ECR


📌 Key Tools

    MLflow: Tracks model artifacts and metadata.

    AWS Lambda: Model deployment target.

    Kinesis: Used to stream predictions.

    Pipenv: For environment management.

    Docker: For reproducible builds and integration tests.

    Pre-commit hooks: Enforce code standards automatically.

🧠 Conceptual Flow

    Model is trained and saved via MLflow.

    MLflow model artifacts are packaged into a Lambda-compatible Docker image.

    Inference requests come from Kinesis (Base64 JSON).

    Lambda decodes, predicts, and optionally streams predictions back to another Kinesis topic.

    Full test coverage is provided from unit → integration.

