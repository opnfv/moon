#!/usr/bin/env bash

VERSION=4.1
export DOCKER_HOST=tcp://172.88.88.1:2376

echo -e "\033[31mDeleting previous dockers\033[m"
docker rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
docker rm -f messenger db keystone consul 2>/dev/null

echo -e "\033[32mStarting Messenger\033[m"
docker run -dti --net=moon --hostname messenger --name messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -e RABBITMQ_HIPE_COMPILE=1 -p 5671:5671 -p 5672:5672 -p 8080:15672 rabbitmq:3-management

echo -e "\033[32mStarting DB manager\033[m"
docker run -dti --net=moon --hostname db        --name db        -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest

docker run -d --net=moon --name=consul --hostname=consul -p 8500:8500 consul

echo "waiting for Database (it may takes time)..."
echo -e "\033[35m"
sed '/ready for connections/q' <(docker logs db -f)
echo -e "\033[m"

echo "waiting for Messenger (it may takes time)..."
echo -e "\033[35m"
sed '/Server startup complete;/q' <(docker logs messenger -f)
echo -e "\033[m"

docker run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka

echo -e "\033[32mConfiguring Moon platform\033[m"
sudo pip install moon_db
moon_db_manager upgrade

cd ${MOON_HOME}/moon_orchestrator
python3 populate_consul.py

echo -e "\033[32mStarting Moon platform\033[m"

docker container run -dti --net moon --hostname orchestrator --name orchestrator wukongsun/moon_orchestrator:${VERSION}
