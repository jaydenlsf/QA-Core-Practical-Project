scp docker-compose.yaml docker-manager:
ssh docker-manager << EOF

export DATABASE_URI=${DATABASE_URI}
docker run -d -p 80:80 --name nginx --mount type=bind,source=$(pwd)/nginx.conf,target=/etc/nginx/nginx.conf nginx:alpine
docker stack deploy --compose-file docker-compose.yaml covid-19-app
docker exec covid-19-app python create.py

EOF