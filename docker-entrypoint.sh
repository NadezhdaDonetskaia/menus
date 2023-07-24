#!/bin/bash

cd app 
poetry run alembic upgrade head
cd ..
poetry run uvicorn --host 0.0.0.0 app.main:app