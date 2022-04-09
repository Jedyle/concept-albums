# syntax=docker/dockerfile:1
FROM python:3.10.4-buster as base

RUN apt-get update -y
RUN apt-get -y install libpq-dev gcc

ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

WORKDIR /app
RUN pip install --upgrade pip==22.0.4
RUN pip install -r requirements.txt


FROM base as prod

COPY ./conceptalbums/ /app/
RUN pip install gunicorn==20.1.0
CMD python manage.py collectstatic --no-input && python manage.py migrate && gunicorn herodotus.wsgi:application --bind 0.0.0.0:8000

