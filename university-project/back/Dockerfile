FROM python:3.11.2-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql postgresql-server-dev-all \
  && apt-get clean


RUN pip install --upgrade pip
COPY src/requirements.txt .
RUN pip install -r requirements.txt


COPY src .
