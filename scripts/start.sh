#!/bin/sh

python app/manage.py collectstatic

exec "$@"
