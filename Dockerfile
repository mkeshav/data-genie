FROM python:3.7 as base

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/

RUN python3 -m pip install -r requirements.txt

FROM base as dev

ADD requirements_dev.txt requirements_dev.txt
RUN python3 -m pip install -r requirements_dev.txt

ADD . /app