FROM python:3.8

USER root

WORKDIR /app

ADD . /app

RUN pip3 install -r requirements.txt

RUN ["chmod", "+x", "/app/docker_run_frontend.sh"]

EXPOSE 8050

CMD /app/docker_run_frontend.sh
