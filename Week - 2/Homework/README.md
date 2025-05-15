# MLflow NYC Taxi Trip Duration Prediction

This project demonstrates a basic workflow for predicting NYC taxi trip duration using MLflow for experiment tracking and model management.

## Project Description

The project consists of the following Python scripts:

* **`preprocess_data.py`**: This script handles data preprocessing. It reads raw Parquet files, calculates trip duration, filters data, performs feature engineering, and saves the processed data and a DictVectorizer.
* **`train.py`**: This script trains a RandomForestRegressor model on the preprocessed training data and logs metrics using MLflow.
* **`hpo.py`**: This script performs hyperparameter optimization for the RandomForestRegressor model using Hyperopt and logs the results with MLflow.
* **`register_model.py`**: This script selects the best model from the hyperparameter optimization runs, logs it with MLflow, and registers it in the MLflow Model Registry.

## Workflow

1.  **Data Preprocessing**: The `preprocess_data.py` script prepares the data for model training.
2.  **Training**: The `train.py` script trains a baseline RandomForestRegressor model.
3.  **Hyperparameter Optimization**: The `hpo.py` script optimizes the model's hyperparameters to improve performance.
4.  **Model Registration**: The `register_model.py` script identifies the best-performing model from the hyperparameter tuning and registers it for deployment.

## MLflow Tracking

MLflow Tracking is a component of MLflow that helps you organize and keep track of your machine learning experiments. In this project, we use it to:

* **Log Parameters**: When we train our models (in `train.py` and `hpo.py`), we record the specific configurations used, such as the number of estimators or the maximum depth of the RandomForestRegressor. This ensures we know exactly what settings were used for each training run.
* **Log Metrics**: After each training run, we evaluate the model's performance using relevant metrics (e.g., RMSE, R-squared) and log these values with MLflow. This allows us to compare different models and hyperparameter settings to see which ones perform best.
* **Log Artifacts**: MLflow also allows us to save files associated with our experiments. In this project, the trained model itself and potentially other relevant files (like the DictVectorizer from preprocessing) are logged as artifacts. This makes it easy to reproduce results and deploy the trained model later.

By using MLflow Tracking, we gain a clear history of our experiments, making it easier to understand the impact of different parameters and identify the best-performing model.