FROM python:3.7-slim as dev

LABEL Author="Keshav Murthy"

ENV SONAR_SCANNER_VERSION 3.3.0.1492
RUN python3 -m pip install --upgrade pip setuptools wheel
RUN python3 -m pip install --user --upgrade twine

RUN mkdir -p /app
WORKDIR /app

COPY requirements* /app/

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r requirements_dev.txt

ADD . /app
ENV PATH="/root/.local/bin:${PATH}"

FROM dev AS sonar
RUN apt-get update && apt-get install -y wget bsdtar
RUN wget -qO- https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip | bsdtar -xvf - -C /root/.local/
RUN chmod +x /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner
RUN chmod +x /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/jre/bin/java
RUN ln -s /root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /root/.local/bin/sonar-scanner
