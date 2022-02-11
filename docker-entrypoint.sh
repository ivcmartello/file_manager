#!/bin/bash

set -e

python manage.py migrate --noinput

# just for test
python manage.py runserver 0.0.0.0:8000
