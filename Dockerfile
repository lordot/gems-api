FROM python:3.11-alpine

RUN mkdir /app

COPY requirements.txt /app

RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r /app/requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

COPY gems_api/ /app

WORKDIR /app

ENTRYPOINT ["sh", "entrypoint.sh"]