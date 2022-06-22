FROM seleniarm/standalone-chromium

COPY . /standalone-chromium
WORKDIR /standalone-chromium

USER root

RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

ENTRYPOINT python3 main.py