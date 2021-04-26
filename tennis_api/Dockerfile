FROM python:3.8-alpine
RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories
RUN apk add --update --no-cache py3-numpy py3-pandas@testing
ENV PYTHONPATH=/usr/lib/python3.8/site-packages

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update
RUN pip install --upgrade pip
RUN apk add python3-dev
RUN apk add gpgme-dev
RUN apk add libc-dev
RUN apk add gcc jpeg-dev zlib-dev libffi-dev freetype-dev musl-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev cairo-dev pango-dev gdk-pixbuf-dev
RUN apk add mariadb-dev
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .