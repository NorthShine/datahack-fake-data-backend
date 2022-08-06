FROM python:3.8-slim

WORKDIR /fake_data_generator

COPY . /fake_data_generator/

RUN apt-get update -y && apt-get upgrade -y
RUN python -m pip install -r requirements.txt &&\
    gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --log-level debub --access-logfile -
