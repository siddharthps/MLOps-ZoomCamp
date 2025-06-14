FROM python:3.11.13-slim-bookworm 

# Upgrade pip and install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY Pipfile Pipfile.lock ./

# Install dependencies via Pipenv in system mode (no virtualenv)
RUN pipenv install --system --deploy

# Copy the application code
COPY predict.py .

# Expose Flask/Gunicorn port
EXPOSE 9696

# Start Gunicorn server pointing to predict.py:app
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "predict:app"]