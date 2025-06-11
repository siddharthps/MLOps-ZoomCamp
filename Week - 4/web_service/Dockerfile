# Use an official slim version of Python 3.12.10 as the base image
FROM python:3.12.10-slim

# Upgrade pip to the latest version to avoid compatibility issues
RUN pip install -U pip

# Install Pipenv, a tool for managing Python dependencies using Pipfile and Pipfile.lock
RUN pip install pipenv

# Set the working directory inside the container to /app
WORKDIR /app

# Copy Pipfile and Pipfile.lock to the working directory (used by Pipenv for dependencies)
COPY [ "Pipfile", "Pipfile.lock", "./" ]

# Install dependencies defined in Pipfile.lock in system mode and fail if lock is outdated
# --system: installs packages into the system Python (not virtualenv)
# --deploy: ensures Pipfile.lock is up to date and will fail otherwise
RUN pipenv install --system --deploy

# Copy the application files to the container
# - predict.py: your main application script
# - lin_reg.bin: serialized model file used for prediction
COPY [ "predict.py", "lin_reg.bin", "./" ]

# Expose port 9696 for external access (gunicorn will bind here)
EXPOSE 9696

# Define the command to run the application using gunicorn
# --bind=0.0.0.0:9696 : listens on all interfaces, port 9696
# predict:app : loads 'app' object from 'predict.py'
ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "predict:app" ]
