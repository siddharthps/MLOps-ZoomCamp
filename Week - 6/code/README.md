## Code snippets

### Building and running Docker images

```bash
docker build -t stream-model-duration:v2 .
```

```bash
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="e1efc53e9bd149078b0c12aeaa6365df" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    stream-model-duration:v2
```

Mounting the model folder:

```
docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="ride_predictions" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-west-1" \
    -v $(pwd)/model:/app/model \
    stream-model-duration:v2
```

### Specifying endpoint URL

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis list-streams
```

```bash
aws --endpoint-url=http://localhost:4566 \
    kinesis create-stream \
    --stream-name ride_predictions \
    --shard-count 1
```

```bash
aws  --endpoint-url=http://localhost:4566 \
    kinesis     get-shard-iterator \
    --shard-id ${SHARD} \
    --shard-iterator-type TRIM_HORIZON \
    --stream-name ${PREDICTIONS_STREAM_NAME} \
    --query 'ShardIterator'
```

### Unable to locate credentials

If you get `'Unable to locate credentials'` error, add these
env variables to the `docker-compose.yaml` file:

```yaml
- AWS_ACCESS_KEY_ID=abc
- AWS_SECRET_ACCESS_KEY=xyz
```

### Make

Without make:

```
isort .
black .
pylint --recursive=y .
pytest tests/
```

With make:

```
make quality_checks
make test
```


To prepare the project, run 

```bash
make setup
```


---

### 📄 `Week - 6/code/README.md`

```markdown
# Lambda-Based ML Inference Service (code/)

This folder contains the code for a **real-time prediction service** built to run as an AWS Lambda function using MLflow for model versioning.

---

## 🔍 Key Files

| File                | Purpose |
|---------------------|---------|
| `lambda_function.py` | Entry point for AWS Lambda. Delegates to model service. |
| `model.py`           | Loads model, handles decoding, feature prep, prediction, and Kinesis output. |
| `Dockerfile`         | Builds a Lambda-compatible container using MLflow + Pipenv. |
| `Makefile`           | Defines build, test, lint, and deployment commands. |
| `Pipfile` / `Pipfile.lock` | Define runtime and dev dependencies using Pipenv. |
| `.pre-commit-config.yaml` | Hooks for `black`, `isort`, `pylint`. |
| `pyproject.toml`     | Formatter + linter configurations. |

---

## 🧠 How Lambda Works

```text
Event (Kinesis Record, base64 JSON)
↓
lambda_handler()
↓
ModelService.lambda_handler()
↓
Base64 decode → feature prep → model.predict() → format response
↓
(Optional) Write to Kinesis


🌍 Environment Variables

| Variable                  | Description                                       |
| ------------------------- | ------------------------------------------------- |
| `RUN_ID`                  | MLflow run ID to locate model                     |
| `MODEL_BUCKET`            | S3 bucket for MLflow artifacts                    |
| `MLFLOW_EXPERIMENT_ID`    | Experiment ID used in S3 path                     |
| `MODEL_LOCATION`          | (Optional) Full S3 path override                  |
| `PREDICTIONS_STREAM_NAME` | Kinesis stream for publishing predictions         |
| `KINESIS_ENDPOINT_URL`    | LocalStack URL for dev/test                       |
| `TEST_RUN`                | When true, disables callbacks like Kinesis writes |


