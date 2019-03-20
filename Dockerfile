FROM python:3

WORKDIR /home/project

COPY requirements.txt requirements.txt

ENV FLASK_APP=project.py

EXPOSE 5000
