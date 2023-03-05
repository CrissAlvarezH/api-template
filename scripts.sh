#!/bin/bash

action=$1


prestart() {
    printf "\n-- init prestart -----------------------\n"

    # Execute migrations
    alembic upgrade head

    # Create default scopes
    python manage.py core create-default-scopes

    # Create super user
    python manage.py core create-superuser

    printf "\n-- finish prestart -----------------------\n"
}


if [ $action = "dev" ]; then
  uvicorn app.main:app --reload

elif [ $action = "start" ]; then
  prestart
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80

elif [ $action = "prestart" ]; then
  prestart

fi