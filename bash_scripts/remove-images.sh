docker rm $(docker ps -a -q)
docker rmi -f $(docker images -f "dangling=true" -q)