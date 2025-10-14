FROM divio/multi-python:latest as dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine mypy

RUN mkdir -p /app
WORKDIR /app

COPY pypirc /root/.pypirc
RUN curl -fLSs https://raw.githubusercontent.com/CircleCI-Public/circleci-cli/master/install.sh | bash

COPY requirements_dev.txt /app/
# test will install the requirements before running the test
RUN python3 -m pip install -r /app/requirements_dev.txt

COPY . /app
ENV PATH="/root/.local/bin:${PATH}"

