#!/bin/bash

curl https://get.docker.com | sudo bash

sudo usermod -aG docker jenkins

docker login -u $DOCKER_LOGIN_USR -p $DOCKER_LOGIN_PSW