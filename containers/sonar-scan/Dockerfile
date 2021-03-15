FROM adoptopenjdk/openjdk11 as dev

LABEL Author="Keshav Murthy"

RUN \
  apt-get update && \
  apt-get install -y \
    python3 python3-pip \
    jq \
    wget \
    zip unzip

ENV SONAR_SCANNER_VERSION 4.6.0.2311
RUN wget -q https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip -P /tmp/
RUN unzip /tmp/sonar-scanner-cli-${SONAR_SCANNER_VERSION}-linux.zip -d /usr/local/
RUN chmod +x /usr/local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner
RUN chmod +x /usr/local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/jre/bin/java
RUN ln -s /usr/local/sonar-scanner-${SONAR_SCANNER_VERSION}-linux/bin/sonar-scanner /usr/bin/sonar-scanner

RUN mkdir -p /sonar-scan
WORKDIR /sonar-scan
COPY sonar-project.properties /sonar-scan/sonar-project.properties
COPY scan /sonar-scan/scan
