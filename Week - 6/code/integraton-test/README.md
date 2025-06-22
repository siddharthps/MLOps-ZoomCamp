
---

### 📄 `Week - 6/code/integraton-test/README.md`

```markdown
# Integration Testing (code/integraton-test/)

This folder contains integration tests that validate the full pipeline in a Dockerized environment — simulating how the Lambda function will behave with real inputs and MLflow models.

---

## 🧪 Test Goals

- Test the Lambda handler with encoded input data
- Ensure model loading works with MLflow artifacts
- Simulate cloud services (e.g., S3, Kinesis) using LocalStack

---

## 🧱 Key Components

| File                   | Purpose |
|------------------------|---------|
| `docker-compose.yaml` | Launches LocalStack (optional) or test environment |
| `event.json`          | Sample Lambda event |
| `run.sh`              | Executes Lambda container with test input |
| `test_docker.py`      | Python-based integration test |
| `test_kinesis.py`     | Placeholder to validate Kinesis behavior |
| `model/MLmodel`       | MLflow model metadata |
| `model/model.pkl`     | Serialized model artifact |
| `model/conda.yaml`    | Environment spec for reproducibility |
| `model/python_env.yaml` | MLflow pyfunc environment for pip installs |

---

## ▶️ Running Integration Tests

```bash
make integration_test
# or directly:
LOCAL_IMAGE_NAME=stream-model-duration:test-tag bash integraton-test/run.sh

This will:

    Build Docker image

    Pass in event.json or encoded input

    Invoke the Lambda handler inside the container

    Print predictions to stdout or Kinesis stream (if configured)

🔍 Notes

    Tests are isolated from actual cloud infra.

    LocalStack can be used if end-to-end AWS simulation is needed.

    Uses base64-encoded input (from data.b64) to simulate Kinesis input.