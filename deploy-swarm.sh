#!/bin/bash

# remove existing containers
docker rm -f $(docker ps -q)

# remove existing images
docker rmi -f $(docker images -q)

# remove existing network with the same name
docker network rm mynetwork

# build image for server
docker build -t jaydenlsf/server server

# build image for country_api
docker build -t jaydenlsf/country_api country_api

# build image for population_api
docker build -t jaydenlsf/population_api population_api

# build image for stats_api
docker build -t jaydenlsf/stats_api stats_api

# push images to docker hub
docker push jaydenlsf/server jaydenlsf/country_api jaydenlsf/population_api jaydenlsf/stats_api:latest

# create a network
docker network create --driver overlay mynetwork

# create app service
docker service create --name covid-19-app -p 5000:5000 --network mynetwork jaydenlsf/server

# create nginx service
docker service create --name nginx -p 80:80 --network jaydenlsf/server --mount type=bind,source=$(pwd)/nginx/nginx.conf,target=/etc/nginx/nginx.conf nginx:alpine

# run containers
# docker run -d -p 5000:5000 --name server --network mynetwork server
# docker run -d --name country_api --network mynetwork country_api
# docker run -d --name population_api --network mynetwork population_api
# docker run -d --name stats_api --network mynetwork stats_apis