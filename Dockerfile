# Production Dockerfile

ARG PYTHON_VERSION=3.10.4-alpine

FROM python:${PYTHON_VERSION} as compile-image

ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1

COPY Pipfile Pipfile.lock ./

RUN \
    apk update && \
    apk upgrade && \
    apk add --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install pipenv && \
    pipenv install --dev --deploy --python 3.10 && \
    apk --purge del .build-deps


FROM python:${PYTHON_VERSION} as runtime

ENV PYTHONUNBUFFERED 1

COPY --from=compile-image /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

WORKDIR /app

RUN \
    apk update && \
    apk upgrade && \
    apk add bash postgresql-libs && \
    rm -rf /var/cache/apk/*

COPY . .

ENV DJANGO_SETTINGS_MODULE core.settings.build

RUN mkdir -p /app/staticfiles && python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "core.wsgi"]
