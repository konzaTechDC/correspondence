FROM python:3.9-alpine3.13

LABEL maintainer = "nkarimi@linux.com"

ENV PYTHONUNBUFFERD 1

COPY ./requirements.txt /requirements.txt

WORKDIR /correspondence
COPY . /correspondence
COPY ./scripts /scripts

EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps \
        build-base postgresql-dev musl-dev linux-headers && \
    apk add postgresql-dev gcc python3-dev musl-dev \
        libc-dev make git libffi-dev openssl-dev libxml2-dev libxslt-dev zlib-dev jpeg-dev && \
    /py/bin/pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home corres_user && \
    # handle static media
    mkdir -p /vol/web/static && \
    mkdir -p /vol/web/media && \
    chown -R corres_user:corres_user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts

ENV PATH="/scripts:/py/bin:$PATH"

USER corres_user

CMD [ "run.sh" ]