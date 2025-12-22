Surveillance et analyse des logs Docker (prototype)

This workspace contains a small FastAPI app and a basic ELK + Filebeat setup to collect container logs.

Quick start

1. Build and start all services (FastAPI, MySQL, Elasticsearch, Kibana, Filebeat):

```bash
docker-compose up -d --build
## fastapi-todo

A small FastAPI TODO web app with a prototype ELK/Filebeat setup for collecting container logs.

### Features
- Simple session-scoped TODOs stored in a SQL database (SQLAlchemy)
- Thin server-rendered frontend using Jinja2 templates
- Basic logging and a test `/error` endpoint for generating log events
- Docker Compose with Elasticsearch, Kibana and Filebeat for log collection (prototype)

<!-- prettier-ignore -->
# fastapi-todo

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

> Surveillance et analyse des logs Docker (prototype)

> This workspace contains a small FastAPI app and a basic ELK + Filebeat setup to collect container logs.

A small FastAPI TODO web app with a prototype ELK/Filebeat setup for collecting container logs.

## Table of Contents
- [Features](#features)
- [Quick Start — Local (Python)](#quick-start--local-python)
- [Quick Start — Docker Compose (includes ELK/Filebeat)](#quick-start--docker-compose-includes-elkfilebeat)
- [Notes about Filebeat and Docker on Windows](#notes-about-filebeat-and-docker-on-windows)
- [Project Layout](#project-layout)
- [Running notes](#running-notes)
- [Troubleshooting](#troubleshooting)
- [Next steps](#next-steps)
- [License](#license)

## Features
- Simple session-scoped TODOs stored in a SQL database (SQLAlchemy)
- Thin server-rendered frontend using Jinja2 templates
- Basic logging and a test `/error` endpoint for generating log events
- Docker Compose with Elasticsearch, Kibana and Filebeat for log collection (prototype)

## Quick Start — Local (Python)
Prerequisites: Python 3.8+, `pip`, and a virtual environment recommended.

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app with Uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. Open the app in your browser: http://127.0.0.1:8000

## Quick Start — Docker Compose (includes ELK/Filebeat)
Build and start all services (FastAPI, MySQL, Elasticsearch, Kibana, Filebeat):

```bash
docker-compose up -d --build
```

Wait for services to become healthy. Common endpoints:
- Kibana: http://localhost:5601
- Elasticsearch: http://localhost:9200

## Notes about Filebeat and Docker on Windows
- Filebeat is configured to read Docker container logs from the host path `/var/lib/docker/containers`. If you run Docker Desktop on Windows, WSL2, or a different host layout, you may need to adjust volume mounts in `docker-compose.yml`.

## Project Layout
- `main.py` — FastAPI application, routes, and simple request-logging middleware
- `models.py` — SQLAlchemy models and helper functions for TODO CRUD
- `database.py` — SQLAlchemy engine and session setup
- `templates/` — Jinja2 templates used by the app (home and todo fragments)
- `docker-compose.yml` — Compose file that includes Elasticsearch/Kibana/Filebeat
- `filebeat/filebeat.yml` — Filebeat configuration to collect container logs

## Running notes
- The app creates the database tables on startup using SQLAlchemy `Base.metadata.create_all(bind=engine)` defined in `main.py`.
- Use the `/error` endpoint to generate an intentional error for testing log collection.

## Troubleshooting
- If the UI doesn't show todos, ensure cookies are enabled — the app uses a `session_key` cookie to scope TODOs.
- If Filebeat doesn't ship logs to Elasticsearch, check container mounts and Filebeat logs: `docker logs filebeat`.

## Next steps
- Harden Elasticsearch for production (enable security, set credentials)
- Add tests and CI for the FastAPI app
- Improve Filebeat parsing / dashboards and add retention policies

## License
See the [LICENSE](LICENSE) file.
