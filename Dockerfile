FROM fkrull/multi-python:latest as dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY pypirc /root/.pypirc

COPY . /app
ENV PATH="/root/.local/bin:${PATH}"