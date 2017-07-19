# Modules for the Moon project

This directory contains all the modules for MoonV4


## Usage

### Prerequist

```bash
sudo apt install python3-dev python3-pip
sudo pip3 install pip --upgrade
sudo apt -y install docker-engine # ([Get Docker](https://docs.docker.com/engine/installation/))
echo 127.0.0.1 messenger db keystone | sudo tee -a /etc/hosts
```

### Install Docker Engine

```bash
sudo apt-get remove docker docker-engine
sudo apt-get install     apt-transport-https     ca-certificates     curl     software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce
sudo docker run hello-world
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart
```

## Launch MySql, RabbitMQ, Keystone

### Cleanup
```bash
docker container rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
docker container rm -f messenger db keystone 2>/dev/null
```


### Internal Network Creation
```bash
docker network create -d bridge --subnet=172.88.88.0/16 --gateway=172.88.88.1 moon
```


### MySql
```bash
docker container run -dti --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest
```

### Rabbitmq
```bash
docker container run -dti --net=moon --hostname messenger --name messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -e RABBITMQ_HIPE_COMPILE=1 -p 5671:5671 -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```


### moon_keystone
```bash
docker container run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 wukongsun/moon_keystone:mitaka
```


## Orchestrator
To start the Moon platform, you have to run the Orchestrator.

### Installation
```bash
sudo pip3 install moon_db --upgrade
sudo pip3 install moon_utilities --upgrade
sudo pip3 install moon_orchestrator  --upgrade
moon_db_manager upgrade
```

### Launch
```bash
moon_orchestrator
```

### Tests
```bash
sudo pip3 install pytest
cd /usr/lib/moon_orchestratr/moon_interface/tests/apitests
pytest
```


## Launch consul, router, manager, interface

### moon_consul
```bash
docker container run -dti --net moon --hostname consul --name consul wukongsun/moon_consul:v4.1
```

### moon_router
```bash
docker container run -dti --net moon --hostname router --name router wukongsun/moon_router:v4.1
```

### moon_manager
```bash
docker container run -dti --net moon --hostname manager --name manager wukongsun/moon_manager:v4.1
```


### moon_interface
```bash
docker container run -dti --net moon --hostname interface --name interface wukongsun/moon_interface:v4.1
```


## Log
### Get some logs
```bash
docker ps
docker logs db
docker logs messenger
docker logs keystone
docker logs router
docker logs manager
docker logs interface
```
