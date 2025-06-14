# 🧠 Duration Prediction Service

A lightweight ML service that predicts trip duration using a trained linear regression model. Served via Flask and Gunicorn inside Docker.

## 🚀 Quickstart

### 1. Build Docker Image
```bash
docker build -t duration-prediction-service:v1 .
```

### 2. Run the Container
```bash
docker run -it --rm -p 9696:9696 duration-prediction-service:v1
```

### 3. Test the API
```bash
python test.py
```

Expected output:
```json
{"duration": <some_float_value>}
```

## 📦 Project Structure

```
.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── predict.py      # Flask app with /predict endpoint
├── lin_reg.bin     # Trained model (pickled)
├── test.py         # Client script to test the API
```

## 🔧 Notes

- Ensure `gunicorn` is listed in `Pipfile`.
- Run `pipenv lock` to regenerate `Pipfile.lock` after dependency changes.
