#!/bin/bash
set -e

python manage.py migrate

exec uvicorn gems_api.asgi:application --host 0.0.0.0