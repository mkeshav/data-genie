FROM divio/multi-python:latest AS dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade pip twine mypy

RUN mkdir -p /app
WORKDIR /app

COPY requirements_dev.txt /app/
# test will install the requirements before running the test
RUN python3 -m pip install -r /app/requirements_dev.txt

COPY pypirc /home/tox/.pypirc
COPY . /app
ENV PATH="/home/tox/.local/bin:${PATH}"

