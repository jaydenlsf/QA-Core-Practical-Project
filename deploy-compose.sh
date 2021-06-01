#!/bin/bash

# remove all running services
docker service rm $(docker service ls -q)

# build docker compose
docker-compose build
docker-compose push

# deploy docker stack
docker stack deploy --compose-file docker-compose.yaml covid-19-app
