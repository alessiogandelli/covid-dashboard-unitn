# syntax=docker/dockerfile:1
FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ["chmod", "+x", "/app/docker_run.sh"]

CMD ./docker_run.sh