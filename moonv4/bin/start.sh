#!/usr/bin/env bash

echo -e "\033[31mDeleting previous dockers\033[m"
docker rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
docker rm -f messenger db keystone 2>/dev/null

echo -e "\033[32mStarting Messenger\033[m"
docker run -dti --net=moon --hostname messenger --name messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -e RABBITMQ_HIPE_COMPILE=1 -p 5671:5671 -p 5672:5672 -p 8080:15672 rabbitmq:3-management

echo -e "\033[32mStarting DB manager\033[m"
docker run -dti --net=moon --hostname db        --name db        -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest

echo waiting for 20 seconds before starting Keystone container...
sleep 20s

docker run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka

echo -e "\033[32mBuilding packages\033[m"
bash $MOON_HOME/bin/build_all.sh

. $MOON_HOME/moon_orchestrator/tests/venv/bin/activate

pip install $MOON_HOME/moon_orchestrator/dist/moon_db-0.1.0.tar.gz --upgrade
pip install $MOON_HOME/moon_orchestrator/dist/moon_utilities-0.1.0.tar.gz --upgrade
echo waiting for 20 seconds before configuring and starting Orchestrator container...
sleep 30s
moon_db_manager upgrade

echo -e "\033[32mStarting Moon Orchestrator\033[m"
moon_orchestrator
