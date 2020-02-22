#!/bin/sh
# #TODO: #FIXME: Get this up to date with https://github.com/pydanny/cookiecutter-django/tree/179adb4f30dfeeace03e6c5fe876e473b0737d02
#python /app/local.py collectstatic --noinput
gunicorn mysite.wsgi:application --bind 0.0.0.0:8000
