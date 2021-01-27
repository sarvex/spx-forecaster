FROM python:3.8.7

WORKDIR /opt/scr/

RUN pip install beautifulsoup4 pandas requests &&\