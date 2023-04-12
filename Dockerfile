FROM python:3.11-slim-buster

RUN mkdir -p /opt/app

ADD ./requirements.txt /opt/app

WORKDIR /opt/app

RUN pip install -r requirements.txt
ADD . /opt/app
