# MLOps ZoomCamp Week 6 Homework

This repository contains the homework completed for Week 6 of the MLOps ZoomCamp, focused on testing, integration with S3, and using Localstack.

## Overview

### Q1: Refactoring and Unit Testing
- Refactored the original batch script to eliminate global variables by creating a `main(year, month)` function.
- Split the data processing logic into separate functions: `read_data` (I/O) and `prepare_data` (transformations).
- Added unit tests covering `prepare_data` using `pytest` to validate data transformations on sample inputs.

### Q4 & Q5: Mocking S3 with Localstack and Creating Test Data
- Set up Localstack with Docker Compose to mock AWS S3 locally.
- Configured environment variables (`INPUT_FILE_PATTERN`, `OUTPUT_FILE_PATTERN`, `S3_ENDPOINT_URL`) for flexible input/output paths.
- Created an integration test script `integration_test.py` that generates test data matching unit test samples and saves it to the mocked S3 bucket (`nyc-duration`).

### Q6: Full Integration Test and Data Saving
- Extended the batch processing script (`q45_batch.py`) to support reading from and writing to S3 via Localstack, respecting environment-configured endpoints.
- Added a `write_data` function for saving results back to S3.
- Developed a comprehensive integration test that:
  - Uploads test input data to Localstack S3,
  - Runs the batch processing container,
  - Downloads the results,
  - Validates the sum of predicted durations programmatically.

## Docker Setup
- Created a `Dockerfile` to containerize the batch processing script.
- Used `docker-compose.yaml` to run Localstack with only the S3 service enabled.
- Built and ran Docker images locally with proper environment variables for Localstack integration.

## Running Tests
- Unit tests run with `pytest` inside a virtual environment managed by `pipenv`.
- Integration tests run inside Docker containers with Localstack mocking S3.
- Provided a PowerShell script `run_integration_test.ps1` for Windows to automate:
  - Building Docker images,
  - Starting Localstack,
  - Creating S3 buckets,
  - Running integration tests.

## Environment Variables
- `INPUT_FILE_PATTERN`: S3 URI pattern for input parquet files.
- `OUTPUT_FILE_PATTERN`: S3 URI pattern for output parquet files.
- `S3_ENDPOINT_URL`: Localstack S3 endpoint URL (e.g., `http://localhost:4566`).
- AWS credentials for Localstack use dummy values (`test`).

## Summary
This homework strengthened skills in:
- Refactoring Python data pipelines for testability,
- Writing unit and integration tests,
- Mocking AWS services locally with Localstack,
- Containerizing applications for consistent environment replication,
- Automating tests and infrastructure setup via scripts.

---
