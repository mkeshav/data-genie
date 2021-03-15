FROM python:3.8 as base

LABEL Author="Keshav Murthy"

ENV SONAR_SCANNER_VERSION 4.6.0.2311
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

FROM dev AS sonar
RUN apt update
RUN apt purge --auto-remove openjdk*
RUN apt install -y default-jdk wget bsdtar
RUN wget -qO- https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip | bsdtar -xvf - -C /root/.local/
RUN chmod +x /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner
RUN chmod +x /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/jre/bin/java
RUN ln -s /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /root/.local/bin/sonar-scanner
