FROM python:3.8 as dev

LABEL Author="Keshav Murthy"

RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/
COPY pypirc /root/.pypirc

RUN python3 -m pip install -r /app/requirements_dev.txt

COPY . /app
ENV PATH="/root/.local/bin:${PATH}"

FROM dev as smoketest
RUN python3 -m pip install data-genie