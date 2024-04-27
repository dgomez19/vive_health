FROM python:3.9-alpine AS build-env

WORKDIR /app

ENV LANG=es_CO.UTF-8
ENV LC_ALL=es_CO.UTF-8
ENV LC_CTYPE=es_CO.UTF8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

RUN apk add --no-cache tzdata
ENV TZ America/Bogota

RUN apk --update add \
    linux-headers \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    libffi-dev \
    jpeg-dev \
    zlib-dev

ARG requirements
COPY ./ /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt


FROM build-env
EXPOSE 8000
