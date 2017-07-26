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

### Configure Docker Engine

```bash
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "hosts": ["tcp://172.88.88.1:2376"]
}
EOF
sudo mv /lib/systemd/system/docker.service /lib/systemd/system/docker.service.bak
sudo sed '/ExecStart=\/usr\/bin\/dockerd -H fd:\/\//ExecStart=\/usr\/bin\/dockerd/' /lib/systemd/system/docker.service.bak | sudo tee /lib/systemd/system/docker.service
sudo service docker restart
export DOCKER_HOST=tcp://172.88.88.1:2376
# if you have a firewall:
sudo ufw allow in from 172.88.88.0/16
```

## Launch MySql, RabbitMQ, Keystone, Consul

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

### moon_consul
```bash
docker run -d --net=moon --name=consul --hostname=consul -p 8500:8500 consul
```


## Orchestrator
To start the Moon platform, you have to run the Orchestrator container.

```bash
docker container run -dti --net moon --hostname router --name router wukongsun/moon_router:v4.1
```

### Tests
```bash
docker exec -ti interface /bin/bash
pip3 install pytest
cd /usr/local/lib/python3.5/dist-packages/moon_interface/tests/apitests
pytest
```


## Launch router, manager, interface, orchestrator independently


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

### moon_orchestrator
```bash
docker container run -dti --net moon --hostname orchestrator --name orchestrator wukongsun/moon_orchestrator:v4.1
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
