# engineer_thesis_api

Simple CRUD REST API resembling real world application's backend. Created for the purpose of my engineering
thesis `Comparison of frontend frameworks`.

## Pre-requisites

- [Python 3.10](https://www.python.org/downloads/)
- [pipenv](https://pypi.org/project/pipenv/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Tools, libraries, frameworks

- Django 4.0, Django REST Framework `django` `djangorestframework`
- `django-cors-headers`
- `django-filter`
- `djangorestframework-simplejwt`
- `django-extensions`
- `drf-spectacular`
- `factory_boy`
- `coverage`

## Setup

Create .venv directory in root directory if you want to have your virtual environment in the project directory (
otherwise it will be created inside pipenv's default .virtualenvs directory somewhere on your computer).

Launch virtual environment with pipenv (it will be created on first run):

```bash
pipenv shell
```

Install dependencies:

```bash
pipenv install
```

### Environment variables

Define environmental variables in dotenv files in ./env directory.

`env/backend.env`

```dotenv
SECRET_KEY=
DJANGO_SETTINGS_MODULE=core.settings.dev
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
```

`env/db.env`

```dotenv
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

### Running the application

Make sure [Docker Engine](https://www.docker.com/products/docker-desktop/) is running.

Building containers (required if Dockerfile or installed packages changed):

```shell
docker compose build
```

Running containers

```shell
docker compose up
```

Executing commands in running containers (e.g. using django cli)

```shell
docker exec -it backend python manage.py migrate
```

```shell
docker exec -it backend python manage.py createsuperuser
```

Bringing down containers

```shell
docker compose down
```

### Testing

Running tests with `coverage`

```shell
docker exec -it backend coverage run manage.py test
```

Coverage report after running unit tests

```shell
docker exec -it backend coverage report -m
```

## Deployment

Todo