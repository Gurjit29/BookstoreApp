FROM python:3

WORKDIR /home/project

COPY requirements.txt requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x initial.sh
RUN ./initial.sh
RUN chmod +x boot.sh
ENV FLASK_APP=project.py

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]