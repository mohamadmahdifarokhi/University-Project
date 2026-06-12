FROM python:3.11.2-slim-bullseye

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get -y install --no-install-recommends netcat gcc libpq-dev \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
COPY src/requirements.txt .
RUN pip install -r requirements.txt


COPY src .
