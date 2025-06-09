This README.md provides a concise overview of the project, detailing the steps undertaken for data processing, model training, and experiment tracking using Mage and MLflow.

## Project Overview

The goal of this project is to create a simple training pipeline for predicting NYC taxi trip durations. The pipeline utilizes Mage for orchestration and MLflow for experiment tracking and model registration. The dataset used is the Yellow taxi data for March 2023.

## Setup and Installation

The project uses Docker for environment setup. The `docker-compose.yml` file defines the services: `magic-platform` (Mage), `magic-database` (PostgreSQL with pgvector), and `mlflow`.

**1. Clone the repository:**

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

**2. Build and run the Docker containers:**

```bash
docker-compose up --build
```

This will start the Mage, PostgreSQL, and MLflow services. Mage will be accessible at `http://localhost:6789`.

## Pipeline Details

The pipeline consists of the following blocks:

### 1. Data Loader (`yellowtaxi_tripdata_dataloader.py`)

* **Purpose:** Loads the Yellow taxi trip data for March 2023 from a public URL.
* **Source:** `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet`
* **Output:** A Pandas DataFrame containing 3,403,766 rows of raw trip data.

### 2. Data Preparation (`yellowtaxi_tripdata_datapreparation.py`)

* **Purpose:** Cleans and preprocesses the loaded data.
* **Transformations:**
    * Converts `tpep_pickup_datetime` and `tpep_dropoff_datetime` to datetime objects.
    * Calculates `duration` in minutes.
    * Filters out trips with `duration` outside the range of 1 to 60 minutes.
    * Converts `PULocationID` and `DOLocationID` to string type.
* **Output:** A processed Pandas DataFrame with a shape of (3,316,216, 20).

### 3. Model Training (`yellowtaxi_tripdata_train_data.py`)

* **Purpose:** Trains a Linear Regression model.
* **Steps:**
    * Creates a `DictVectorizer` using `PULocationID` and `DOLocationID`.
    * Trains a `LinearRegression` model using the vectorized features and `duration` as the target.
* **Output:**
    * The fitted `DictVectorizer` object.
    * The trained `LinearRegression` model.
* **Model Intercept:** The intercept of the trained model is approximately 24.78.

### 4. Model Exporter (`yellowtaxi_tripdata_data_export.py`)

* **Purpose:** Registers the trained model and preprocessor with MLflow.
* **MLflow Configuration:**
    * `TRACKING_URI`: `http://mlflow:5001`
    * `EXPERIMENT_NAME`: `homework-03`
    * `developer` tag: `gabi`
    * `mlflow.sklearn.autolog()` is enabled.
* **Actions:**
    * Saves the `DictVectorizer` (preprocessor) as an artifact.
    * Logs the `LinearRegression` model to MLflow.
    * Registers the model under the name "linear-reg-model".
* **Model Size:** The size of the logged model (model\_size\_bytes) is 4534 bytes.

## Mage and MLflow Integration

* **Mage Version:** `v0.9.73`
* **Mage Project:** A project named `homework_03` was created, resulting in a `metadata.yaml` file with 55 lines.
* **MLflow UI:** The MLflow UI is accessible at `http://localhost:5001` and can be used to track experiments, view logged parameters, metrics, artifacts, and registered models.

## How to Run

1.  Ensure Docker is running on your machine.
2.  Follow the "Setup and Installation" steps.
3.  Access the Mage UI at `http://localhost:6789`.
4.  Navigate to the `homework_03` project.
5.  Run the pipeline to execute the data loading, preparation, training, and model export steps.
6.  Access the MLflow UI at `http://localhost:5001` to view the logged experiments and registered models.