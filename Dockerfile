FROM python:3.6.8-alpine

ENV PYTHONBUFFERED 1
ENV DJANGO_ENV dev
ENV DOCKER_CONTAINER 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

RUN apk update \
    && apk add libffi-dev openssl-dev libressl-dev jpeg-dev zlib-dev \
    && apk add --upgrade make \
    && apk add --virtual build-deps \
    && apk add gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

COPY ./requirements.txt /code/requirements.txt
RUN pip install -r /code/requirements.txt

RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

COPY . /code/
WORKDIR /code/

USER 1000

EXPOSE 8080