FROM python:3

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY poetry.lock /app
COPY pyproject.toml /app
COPY ./innotter/innotter/.env /app/inotter/innotter/innotter

RUN pip3 install poetry

RUN poetry install