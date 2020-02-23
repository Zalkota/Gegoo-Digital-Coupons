#!/bin/bash

python local.py migrate
python /app/local.py collectstatic --noinput
# Prepare log files and start outputting logs to stdout
RUN mkdir logs
touch ./logs/gunicorn.log
touch ./logs/gunicorn-access.log
tail -n 0 -f ./logs/gunicorn*.log &

# export DJANGO_SETTINGS_MODULE=mysite.settings.dev

exec gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=./logs/gunicorn.log \
    --access-logfile=./logs/gunicorn-access.log \
"$@"
