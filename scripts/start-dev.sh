#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o xtrace

python manage.py migrate
python manage.py collectstatic --noinput --verbosity 0
python manage.py createsuperuser --noinput || true

uvicorn passport_checker.asgi:application --host 0.0.0.0 --port 8000 --reload