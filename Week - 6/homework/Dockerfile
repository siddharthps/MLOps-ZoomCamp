FROM python:3.10.9-slim

RUN pip install -U pip & pip install pipenv

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "q45_batch.py", "q45_batch.py" ]
COPY [ "model.bin", "model.bin" ]

ENTRYPOINT [ "python", "q45_batch.py" ]