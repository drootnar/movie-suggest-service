#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

cd suggest_service  
su -m myuser -c "celery worker -A suggest_service.celeryconf -Q default -n default@%h -l info --beat"