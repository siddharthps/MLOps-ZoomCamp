import os
import mlflow
from mlflow.tracking import MlflowClient
from flask import Flask, request, jsonify

MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI", "http://localhost:5001"
)
EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "green-taxi-duration-mlflow")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

def get_latest_run_id(experiment_name: str) -> str:
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        raise RuntimeError(f"Experiment '{experiment_name}' not found in MLflow.")
    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        order_by=["attributes.start_time DESC"],
        max_results=1
    )
    if not runs:
        raise RuntimeError(f"No runs found for experiment '{experiment_name}'.")
    return runs[0].info.run_id

try:
    RUN_ID = get_latest_run_id(EXPERIMENT_NAME)
    print(f"Loaded latest run ID: {RUN_ID}")
except Exception as e:
    print(f"Error fetching latest run ID: {e}")
    raise

logged_model_uri = f"runs:/{RUN_ID}/model"
model = mlflow.pyfunc.load_model(logged_model_uri)

def prepare_features(ride):
    return {
        "PU_DO": f"{ride['PULocationID']}_{ride['DOLocationID']}",
        "trip_distance": ride["trip_distance"],
    }

def predict_single(ride):
    features = prepare_features(ride)
    preds = model.predict([features])
    return float(preds[0])

app = Flask("duration-prediction")

@app.route("/predict", methods=["POST"])
def predict_endpoint():
    ride = request.get_json()
    duration = predict_single(ride)
    return jsonify({"duration": duration, "model_version": RUN_ID})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9696, debug=False)
