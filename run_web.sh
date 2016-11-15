#!/bin/sh

# wait for PSQL server to start
sleep 10

cd suggest_service
su -m myuser -c "python manage.py makemigrations suggest_service"
su -m myuser -c "python manage.py migrate"  
su -m myuser -c "python manage.py runserver 0.0.0.0:8000" 