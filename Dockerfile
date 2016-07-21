FROM python:3.5.2-alpine

ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN set -x \
    && addgroup -S app \
    && adduser -D -S -h /usr/src/app -s /sbin/nologin -G app app app \
    && apk add --update --virtual .build-deps \
        musl-dev \
        gcc \
    && apk add --virtual .run-deps \
        libjpeg-turbo-dev \
        zlib-dev \
        freetype-dev \
        libpng-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/*

COPY . /usr/src/app

EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "-w", "4", "wsgi:application"]
