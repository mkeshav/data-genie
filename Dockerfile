FROM python:3.8 as dev

LABEL Author="Keshav Murthy"

ENV SONAR_SCANNER_VERSION 4.6.0.2311
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

FROM dev AS sonar
RUN apt update
RUN apt purge --auto-remove openjdk*
RUN apt install -y default-jdk wget bsdtar
RUN wget -qO- "https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip" | bsdtar -xvf - -C /root/.local/
RUN chmod +x "/root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner"
RUN chmod +x "/root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/jre/bin/java"
RUN ln -s "/root/.local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner" /root/.local/bin/sonar-scanner
