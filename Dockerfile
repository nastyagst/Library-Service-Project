FROM python:3.12-alpine
LABEL maintainer="hociy2015@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r requirements.txt

RUN apk del .tmp-build-deps

COPY . .

RUN adduser --disabled-password --no-create-home django-user
USER django-user