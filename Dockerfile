FROM python:3.7 as dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/

RUN python3 -m pip install -r requirements.txt

ADD . /app
ENV PATH="/root/.local/bin:${PATH}"