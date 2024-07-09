#!/bin/sh
set -e
# Run Alembic migrations
alembic upgrade head
#Run fastapi app
uvicorn smart_vendor.main:app --host 0.0.0.0 --port 80