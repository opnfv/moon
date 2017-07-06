#!/usr/bin/env bash

SLAVE_NAME=$1

apt-get update
apt-get install -y python3-dev python3-pip git
pip3 install pip --upgrade
echo 127.0.0.1 messenger db keystone | tee -a /etc/hosts
apt-get install -y    apt-transport-https     ca-certificates     curl     software-properties-common
apt-get update

curl -sSL https://get.docker.com | sh
docker run hello-world
groupadd docker
gpasswd -a ${USER} docker
service docker restart

cd
git clone https://git.opnfv.org/moon
cd moon/moonv4
export MOON_HOME=$(pwd)
sudo ln -s $(pwd)/moon_orchestrator/conf /etc/moon
sudo cp /vagrant/conf/moon_${SLAVE_NAME}.conf /et/moon/moon.conf

docker network create -d bridge --subnet=172.18.0.0/16 --gateway=172.18.0.1 moon
docker load -i /vagrant/keystone.tar

docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
docker run -dti  --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest

bash ${MOON_HOME}/bin/build_all.sh

cd ${MOON_HOME}/moon_orchestrator
pip3 install pip --upgrade
source ${MOON_HOME}/bin/build_all.sh
pip3 install -r requirements.txt --upgrade
pip3 install ${MOON_HOME}/moon_orchestrator/dist/moon_db-0.1.0.tar.gz --upgrade
pip3 install ${MOON_HOME}/moon_orchestrator/dist/moon_utilities-0.1.0.tar.gz --upgrade
pip3 install .  --upgrade

echo "waiting for Database (it may take time)..."
echo -e "\033[35m"
sed '/ready for connections/q' <(docker logs db -f)
echo -e "\033[m"

echo "waiting for Messenger (it may take time)..."
echo -e "\033[35m"
sed '/Server startup complete;/q' <(docker logs messenger -f)
echo -e "\033[m"


docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone_mitaka:latest

echo moon_orchestrator
