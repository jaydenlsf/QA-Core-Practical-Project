scp docker-compose.yaml swarm-master:
ssh swarm-master << EOF

export DATABASE_URI=${DATABASE_URI}
docker stack deploy --compose-file docker-compose.yaml covid-19-app
docker exec covid-19-app python create.py

EOF