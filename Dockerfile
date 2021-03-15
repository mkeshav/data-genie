FROM python:3.8-slim as base

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

FROM base as dev
COPY requirements* /app/

RUN python3 -m pip install -r /app/requirements.txt
RUN python3 -m pip install -r /app/requirements_dev.txt

ADD . /app
ENV PATH="/root/.local/bin:${PATH}"

FROM base as smoketest
COPY smoke_test.py /app/
RUN python3 -m pip install data-genie