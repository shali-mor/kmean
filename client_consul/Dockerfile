FROM python:3.5.1-alpine
MAINTAINER  shmor@cisco.com

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY kmean-consul.py pairs.json  point.py cluster.py requirements.txt   /usr/src/app/




