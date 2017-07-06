#!/usr/bin/env bash

docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
docker run -dti  --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest

echo "waiting for Database (it may take time)..."
echo -e "\033[35m"
sed '/ready for connections/q' <(docker logs db -f)
echo -e "\033[m"

echo "waiting for Messenger (it may take time)..."
echo -e "\033[35m"
sed '/Server startup complete;/q' <(docker logs messenger -f)
echo -e "\033[m"


docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 asteroide/keystone_mitaka:latest

moon_db_manager up

moon_orchestrator
