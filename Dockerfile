FROM fkrull/multi-python:latest as dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY requirements_dev.txt /app/
COPY pypirc /root/.pypirc

# test will install the requirements before running the test
RUN python3 -m pip install -r /app/requirements_dev.txt

COPY . /app
ENV PATH="/root/.local/bin:${PATH}"

FROM python:3.8 as smoketest
RUN python3 -m pip install data-genie