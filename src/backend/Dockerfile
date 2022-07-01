FROM openjdk:slim
COPY --from=python:3.8 / /

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN ["curl", "-O", "https://jdbc.postgresql.org/download/postgresql-42.4.0.jar"]
RUN ["chmod", "+x", "/app/docker_run.sh"]

CMD /app/docker_run.sh