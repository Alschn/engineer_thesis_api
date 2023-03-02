FROM python:3.10.4-alpine as compile-image

ENV PYTHONUNBUFFERED=1
ENV PIPENV_VENV_IN_PROJECT=1

COPY Pipfile Pipfile.lock ./

RUN \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install pipenv && \
    pipenv install --dev --deploy --python 3.10 && \
    apk --purge del .build-deps

FROM python:3.10.4-alpine as runtime

ENV PYTHONUNBUFFERED=1

COPY --from=compile-image /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

RUN \
    apk update && \
    apk upgrade && \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

COPY . .

EXPOSE 8000
