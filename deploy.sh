#!/bin/bash

# remove existing containers
docker rm -f $(docker ps -q)

# remove existing images
docker rmi -f $(docker images -q)

# remove existing network with the same name
docker network rm mynetwork

# build image for server
docker build -t server server

# build image for country_api
docker build -t country_api country_api

# build image for population_api
docker build -t population_api population_api

# build image for stats_api
docker build -t stats_api stats_api

# create a network
docker network create mynetwork

# run containers
docker run -d -p 5000:5000 --name server --network mynetwork server
docker run -d --name country_api --network mynetwork country_api
docker run -d --name population_api --network mynetwork population_api
docker run -d --name stats_api --network mynetwork stats_api