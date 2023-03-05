<div align="center" style="padding-bottom: 20px">
    <h1>engineer_thesis_api</h1>
    <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt=""/>&nbsp;
    <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt=""/>&nbsp;
    <img src="https://img.shields.io/badge/Django-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray" alt=""/>&nbsp;
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt=""/>&nbsp;
    <img src="https://img.shields.io/badge/Docker-008FCC?style=for-the-badge&logo=docker&logoColor=white" alt=""/>&nbsp;
    <img src="https://img.shields.io/badge/Fly.io-7B36ED?style=for-the-badge&logo=fly.io&logoColor=white" alt=""/>&nbsp;
</div>

Simple CRUD REST API resembling real world application's backend. Created for the purpose of my engineering
thesis `Comparison of frontend frameworks`.

## Pre-requisites

- [Python 3.10](https://www.python.org/downloads/)
- [pipenv](https://pypi.org/project/pipenv/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- [Fly.io CLI](https://fly.io/docs/getting-started/installing-flyctl/)

## Tools, libraries, frameworks

- Django 4.0, Django REST Framework `django` `djangorestframework`
- `django-cors-headers`
- `django-filter`
- `djangorestframework-simplejwt`
- `django-extensions`
- `drf-spectacular`
- `factory_boy`
- `coverage`
- `psycopg2`
- `gunicorn`
- `whitenoise`

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

Useful links:

- [Fly.io Docs](https://fly.io/docs/)
- [Fly.io CLI](https://fly.io/docs/flyctl/)
- [Fly.io Dashboard](https://fly.io/dashboard/)

### Launch

To configure and launch the app, run the `fly launch` command and follow the wizard.
You need to provision a Postgres database before launching the app.

### Environment variables

Set environment variables in Fly.io dashboard or via `flyctl` cli.

```dotenv
SECRET_KEY=...
PRODUCTION_HOST=engineer-thesis-api.fly.dev
CLIENT_APP_REACT=https://engineer-thesis-react.vercel.app
CLIENT_APP_SVELTE=https://engineer-thesis-svelte.vercel.app
```

```shell
fly secrets set VARIABLE=...
```

### GitHub secrets

Obtain Fly.io API key and add it as a secret to your repository to enable continuous deployments.

```shell
fly auth token
```

### Manual deployment

```shell
fly deploy
```

### Connect to a running instance

```shell
fly ssh console
```
