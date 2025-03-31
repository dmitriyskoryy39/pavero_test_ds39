FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1

RUN mkdir /app
WORKDIR /app
EXPOSE 8008

ADD requirements.txt .
RUN pip install -U pip && pip install -r requirements.txt

COPY .env .
COPY . .
