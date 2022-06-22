FROM seleniarm/standalone-chromium

COPY . /standalone-chromium
WORKDIR /standalone-chromium

USER root

RUN apt-get update
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

ENV SCREEN_WIDTH=1920
ENV SCREEN_HEIGHT=1080

WORKDIR /standalone-chromium/tests
# ENTRYPOINT pytest -vv