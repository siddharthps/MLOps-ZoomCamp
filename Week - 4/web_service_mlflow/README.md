Here's a detailed `README.md` file for your MLOps project, covering the purpose of each file, how to run the system, and the valuable troubleshooting lessons learned.

---

# MLOps with MLflow and Docker Compose: NYC Yellow Taxi Duration Prediction

This project demonstrates a basic MLOps setup using MLflow for experiment tracking and model management, and Docker Compose for orchestrating a training service, an MLflow tracking server, and a model prediction service. The goal is to train a model to predict NYC Yellow Taxi trip durations and serve predictions via a web API.

## Project Structure

```
.
├── docker-compose.yml
├── Dockerfile
├── Dockerfile.trainer
├── Pipfile
├── Pipfile.lock
├── predict.py
├── random-forest.py
├── test.py
├── mlflow_data/   (created by Docker Compose)
└── mlruns/        (created by Docker Compose)
```

### File and Folder Descriptions:

* **`docker-compose.yml`**:
    * This is the heart of the orchestration. It defines three services:
        * `mlflow-server`: The MLflow tracking server, which stores metadata about runs (parameters, metrics) and artifacts (models).
        * `model-trainer`: A service that trains a Random Forest model for taxi trip duration prediction and logs it to the `mlflow-server`.
        * `duration-prediction`: A Flask web service that loads the latest model from MLflow and serves predictions via an API endpoint.
    * It defines how these services interact, share data (volumes), and expose ports.

* **`Dockerfile`**:
    * This is the Dockerfile for the `duration-prediction` service. It builds the image containing the Python environment and the Flask application (`predict.py`) that will serve predictions.

* **`Dockerfile.trainer`**:
    * This Dockerfile specifically builds the image for the `model-trainer` service. It sets up the Python environment required to run `random-forest.py` and interact with MLflow.

* **`Pipfile`** and **`Pipfile.lock`**:
    * These files are used by `pipenv` for dependency management. They define the Python packages required for the project (both training and prediction environments) and ensure reproducible builds.

* **`predict.py`**:
    * This Python script contains the Flask application logic for the prediction service.
    * It's responsible for:
        * Connecting to the MLflow tracking server.
        * Identifying and loading the latest trained model from a specific MLflow experiment (`green-taxi-duration-mlflow`).
        * Exposing a `/predict` API endpoint that accepts trip data and returns duration predictions.

* **`random-forest.py`**:
    * This Python script implements the model training process.
    * It performs data loading, preprocessing, trains a Random Forest Regressor, and crucially, logs the model, parameters, and metrics to the configured MLflow tracking server.
    * It specifically uses the experiment name `green-taxi-duration-mlflow`.

* **`test.py`**:
    * A simple Python script used to send a sample request to the `duration-prediction` web service's API endpoint (http://localhost:9696/predict) and print the prediction.

* **`mlflow_data/` (Directory)**:
    * This directory is created on your host machine and serves as the persistent storage for the MLflow **backend store**.
    * Inside this directory, MLflow will store its database file (e.g., `mlflow.db`), which contains all the metadata (run IDs, parameters, metrics, etc.).
    * It's mounted into the `mlflow-server` container at `/mlflow`, and the database is configured to be `sqlite:///mlflow/mlflow.db`.

* **`mlruns/` (Directory)**:
    * This directory is created on your host machine and serves as the persistent storage for the MLflow **artifact store**.
    * MLflow stores the actual model files and other artifacts (plots, data, etc.) here.
    * It's mounted into the `mlflow-server`, `model-trainer`, and `duration-prediction` containers consistently at `/mlflow/artifacts` to ensure all services can access the artifacts.

## Setup and Running the Project

### Prerequisites

* Docker Desktop (or Docker Engine) installed and running.
* Python (for running `test.py` locally and managing `pipenv`).
* `pipenv` (optional, but used for dependency management in Dockerfiles).

### Steps to Run

It's crucial to follow these steps sequentially, especially during initial setup, to ensure all dependencies are met before starting dependent services.

1.  **Navigate to the project directory:**
    ```bash
    cd C:\Users\Siddharth\Downloads\MLOps ZoomCamp\Week - 4\web_service_mlflow
    ```

2.  **Clean up any previous Docker containers/data (highly recommended for a fresh start):**
    ```bash
    docker-compose down --volumes --rmi all
    ```
    This command stops all services, removes containers, networks, and volumes (including `mlflow_data` and `mlruns` on your host if they were created as Docker volumes, but since you're using bind mounts `mlruns` and `mlflow_data` directly, you might need to manually delete them if you want a *completely* fresh start for those host directories).

3.  **Start *only* the MLflow Tracking Server:**
    This service needs to be running *before* the model trainer can log anything to it.
    ```bash
    docker-compose up -d mlflow-server
    ```
    Verify it's running:
    ```bash
    docker ps
    # You should see 'web_service_mlflow-mlflow-server-1' listed as Up.
    ```
    You can access the MLflow UI at `http://localhost:5001`.

4.  **Run the Model Trainer (as a one-off command):**
    This command will build the `model-trainer` image (if not already built), run the `random-forest.py` script, which connects to the running `mlflow-server` to log the model. The container will then exit after completion.
    ```bash
    docker-compose run --rm model-trainer
    ```
    * **Wait for this command to complete fully.** You will see output from the training script, including a "View run..." URL from MLflow. This indicates the model has been trained and successfully logged.
    * The `--rm` flag ensures the temporary trainer container is removed after it exits.

5.  **Start the Prediction Service:**
    Now that the model has been logged, the `duration-prediction` service can start and successfully load it.
    ```bash
    docker-compose up -d duration-prediction
    ```
    Verify both services are running:
    ```bash
    docker ps
    # You should now see both 'web_service_mlflow-mlflow-server-1' and 'web_service_mlflow-duration-prediction-1' as Up.
    ```

6.  **Check Prediction Service Logs (Optional, but good for verification):**
    To confirm the prediction service started correctly and loaded the model:
    ```bash
    docker-compose logs duration-prediction
    # Look for messages indicating successful model loading.
    ```

7.  **Test the Prediction Endpoint:**
    Finally, send a test request to your running prediction service:
    ```bash
    python test.py
    ```
    You should see a prediction output similar to:
    `Prediction: {'duration': 45.50965007660853, 'model_version': 'd07cbaab12494f1db06648ca1a7a4638'}`

## Troubleshooting and Key Learnings

Throughout this setup process, several common issues were encountered and resolved, providing valuable insights into Docker Compose orchestration and MLflow integration.

### 1. Error: `RuntimeError: Experiment 'green-taxi-duration-mlflow' not found in MLflow.`

* **Description:** The `duration-prediction` service would start and immediately crash with this error, even though `docker-compose up -d` indicated containers were starting. `docker ps` showed the `duration-prediction` container wasn't running.
* **Cause:** This was primarily a **race condition** and a misunderstanding of how `depends_on: service_completed_successfully` behaves with `docker-compose up -d`. While the `docker-compose.yml` specified this dependency, `docker-compose up -d` often attempts to orchestrate container starts concurrently. The `duration-prediction` service was attempting to load the model *before* the `model-trainer` had fully completed its run and logged the model to MLflow.
* **Resolution:** Enforcing a **strictly sequential startup** process:
    1.  Start `mlflow-server` first.
    2.  Run `model-trainer` as a *one-off command* (`docker-compose run --rm model-trainer`) and wait for it to fully complete and log the model.
    3.  Then, start `duration-prediction`.
* **Lesson Learned:** For services with hard dependencies on a preceding task (like model logging) that might be short-lived, relying solely on `depends_on` with `service_completed_successfully` in a `docker-compose up -d` command can be unreliable due to subtle timing windows. Manual sequential startup or implementing retry logic within the dependent application (e.g., `predict.py` trying to load the model in a loop) is often necessary for robust automation.

### 2. Error: `mlflow.exceptions.MlflowException: The following failures occurred while downloading one or more artifacts from /mlflow/artifacts/... [Errno 2] No such file or directory`

* **Description:** After resolving the "Experiment not found" error, the `duration-prediction` service would still crash, but with an error indicating that MLflow couldn't find the artifact files on the file system, even though the MLflow tracking server knew about the run ID.
* **Cause:** A **misalignment in Docker volume mounts**.
    * `mlflow-server` was configured to store artifacts at `/mlflow/artifacts` inside its container (mapped to `./mlruns` on the host).
    * However, `duration-prediction` was mounting the *same host directory* (`./mlruns`) to a *different path* inside its container (`/app/mlruns`).
    * When `predict.py` in `duration-prediction` tried to load the model (e.g., from `runs:/<RUN_ID>/model`), the MLflow client library internally expected the artifacts to be at the path configured by the MLflow server (`/mlflow/artifacts/...`). But that path didn't exist in the `duration-prediction` container; the data was at `/app/mlruns/...`.
* **Resolution:** Modified `docker-compose.yml` to ensure all services that need to read or write MLflow artifacts mounted the host's `mlruns` directory to the **same consistent path** inside their respective containers, specifically `/mlflow/artifacts`.
    * `volumes: - ./mlruns:/mlflow/artifacts` was applied to `mlflow-server`, `model-trainer`, and `duration-prediction`.
* **Lesson Learned:** When using shared volumes (especially for data stores like MLflow artifacts), ensure that all containers accessing that data mount it to the *exact same internal path* if the application expects a specific absolute path or relies on the tracking server's configuration for artifact roots. Consistency is key for inter-container file system access.

### 3. Error: `mlflow server Error: Got unexpected extra arguments (# Server explicitly uses /mlflow/artifacts)`

* **Description:** The `mlflow-server` itself failed to start with this parsing error after a `docker-compose.yml` modification.
* **Cause:** YAML parsing of `command` blocks in Docker Compose. When using the `>` (block scalar) syntax for a multi-line command, any line indented below it is treated as part of the command string, including lines starting with `#`. Docker Compose does not automatically strip shell-style comments from within a `command` string.
* **Resolution:** Removed the comment line (`# Server explicitly uses /mlflow/artifacts`) from directly within the `command` block of the `mlflow-server` service. Comments should be placed outside the `command` block or on separate lines if the `command` itself is a single string.
* **Lesson Learned:** Pay close attention to YAML syntax and how Docker Compose interprets multi-line strings, especially within `command` blocks. Comments directly within a command block can be interpreted as arguments, leading to unexpected errors.

