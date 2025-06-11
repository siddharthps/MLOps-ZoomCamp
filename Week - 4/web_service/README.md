🧠 Duration Prediction Service

A lightweight ML service that predicts trip duration using a trained linear regression model. Served via Flask and Gunicorn inside Docker.
🚀 Quickstart
1. Build Docker Image

docker build -t duration-prediction-service:v1 .

2. Run the Container

docker run -it --rm -p 9696:9696 duration-prediction-service:v1

3. Test the API

python test.py

Expected output:

{"duration": <some_float_value>}

📦 Project Structure

.
├── Dockerfile
├── Pipfile
├── Pipfile.lock
├── predict.py      # Flask app with /predict endpoint
├── lin_reg.bin     # Trained model (pickled)
├── test.py         # Client script to test the API

🔧 Notes

    Make sure gunicorn is listed in the Pipfile.

    Regenerate Pipfile.lock after adding dependencies: pipenv lock.