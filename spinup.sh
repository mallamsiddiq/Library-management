#!/bin/bash

# Run commands inside the running "web" container
echo Spinning up

docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate

docker-compose run web python manage.py runserver 127.0.0.1:8000