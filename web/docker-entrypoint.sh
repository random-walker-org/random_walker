#!/bin/bash
echo Starting postgres
exec start-stop-daemon --start --chuid postgres:postgres \
     --exec /usr/lib/postgresql/9.3/bin/postgres -- \
     -D /var/lib/postgresql/9.3/main \
     -c config_file=/etc/postgresql/9.3/main/postgresql.conf &

## Remove copied migrations
rm -r random_walker_engine/migrations/*
touch random_walker_engine/migrations/__init__.py
rm -r user_action/migrations/*
touch user_action/migrations/__init__.py

## Make migration
python manage.py makemigrations --setting=settings.local_docker_single
python manage.py migrate --setting=settings.local_docker_single

## Collect static files
python manage.py collectstatic --noinput --setting=settings.local_docker_single

## Create log directory for uwsgi
mkdir -p /var/log/uwsgi/

## Move uwsgi configuration file to appropriate location
mkdir -p /etc/uwsgi/sites/
mv random_walker.ini /etc/uwsgi/sites/
mv uwsgi.conf /etc/init/

## Move Nginx configuration to appropriate location
mv random_walker.conf /etc/nginx/sites-available/
ln -fs /etc/nginx/sites-available/random_walker.conf /etc/nginx/sites-enabled

## Start the web and application server.
# service uwsgi start
# uwsgi --emperor /etc/uwsgi/sites --gid www-data --uid root&
uwsgi --ini /etc/uwsgi/sites/random_walker.ini --gid www-data --uid root &
service nginx start


