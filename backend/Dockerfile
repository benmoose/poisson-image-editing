FROM python:3-alpine

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code
RUN pip install -r requirements.txt
ADD . /code
