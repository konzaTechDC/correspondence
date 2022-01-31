FROM python:3.9-alpine3.13

LABEL maintainer = "nkarimi@linux.com"

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt

WORKDIR /correspondence
COPY . /correspondence
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev && \
    apk add postgresql-dev gcc python3-dev musl-dev \
        libc-dev make git libffi-dev openssl-dev libxml2-dev libxslt-dev zlib-dev jpeg-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home corres_user

ENV PATH="/py/bin:$PATH"

USER corres_user