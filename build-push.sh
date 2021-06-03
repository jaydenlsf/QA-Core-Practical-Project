docker rm -f $(docker ps -qa)
docker-compose up -d --build
docker exec covid-19-app python create.py
# docker login
# docker-compose push