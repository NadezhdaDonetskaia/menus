#!/bin/bash

set -x

source .env
export DATABASE_URL=$DATABASE_URL_TEST 

poetry run alembic upgrade head
poetry run pytest