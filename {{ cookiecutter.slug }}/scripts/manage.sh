#!/bin/bash

echo "Manage: migrating"
python /app/manage.py makemigrations
python /app/manage.py migrate
python /app/manage.py collectstatic --noinput --clear
echo "Manage: done"
