#!/bin/bash

rm .venv -r
poetry install
poetry run alembic upgrade head
poetry run uvicorn --host 0.0.0.0 main:app --reload
