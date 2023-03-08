#!/bin/bash

action=$1


log() {
  GREEN='\033[0;32m'
  YELLOW="\033[0;33m"
  COLOR_OFF="\033[0m"

  if [ "$2" = "warn" ]; then
    color="$YELLOW"
  else
    color="$GREEN"
  fi

  printf "\n${color}$1${COLOR_OFF}\n"
}


prestart() {
    log "-- init prestart -----------------------"

    python manage.py core wait-for-db-available

    # Execute migrations
    alembic upgrade head

    # Create default scopes
    python manage.py core create-default-scopes

    # Create super user
    python manage.py core create-superuser

    log "-- finish prestart -----------------------"
}


build_img() {
    version=$1
    [ -z "$version" ] && version=0.1 && log "set default version 0.1"

    docker build --no-cache -t crissalvarezh/api-template:$version .

    docker tag crissalvarezh/api-template:$version crissalvarezh/api-template:latest

    log "Finish build image"
}


push_img() {
    version=$1
    [ -z "$version" ] && version=0.1 && log "set default version 0.1"

    docker push crissalvarezh/api-template:$version
    docker push crissalvarezh/api-template:latest

    log "Finish push image"
}


if [ ! -x "$(command -v docker-compose)" ]; then
    log "WARN: docker-compose doesn't exist, use alias for 'docker compose'" "warn"
    alias docker-compose='docker compose'
fi


if [ $action = "dev" ]; then
  uvicorn app.main:app --reload

elif [ $action = "setup" ]; then
	docker-compose up -d database

elif [ $action = "up" ]; then
	docker-compose up -d api

elif [ $action = "start" ]; then
  prestart
  uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80

elif [ $action = "prestart" ]; then
  prestart

elif [ $action = "publish" ]; then
  build_img $2
  push_img $2

elif [ "$action" = "deploy" ]; then
  server_user=$2
  server_address=$3

  ssh -o StrictHostKeyChecking=no \
      -i ./server-key.pem $server_user@$server_address \
      "cd /home/ec2-user/api-template && make reload-service"

elif [ "$action" = "reload-service" ]; then
  log "pull images"
  docker-compose pull api

  log "relaunch service"
  docker-compose up --force-recreate --no-deps -d api
  docker image prune -f

  log "Finish reload service"
fi