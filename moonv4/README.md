# Moon Version 4

This directory contains all the modules for MoonV4


## Installation
### Prerequisite
```bash
sudo apt install python3-dev python3-pip
sudo pip3 install pip --upgrade
sudo apt -y install docker-engine # ([Get Docker](https://docs.docker.com/engine/installation/))
echo 127.0.0.1 messenger db keystone | sudo tee -a /etc/hosts
```


### Docker Engine Configuration
```bash
cat <<EOF | sudo tee /etc/docker/daemon.json
{
  "hosts": ["fd://", "tcp://0.0.0.0:2376"]
}
EOF
sudo mv /lib/systemd/system/docker.service /lib/systemd/system/docker.service.bak
sudo sed 's/ExecStart=\/usr\/bin\/dockerd -H fd:\/\//ExecStart=\/usr\/bin\/dockerd/' /lib/systemd/system/docker.service.bak | sudo tee /lib/systemd/system/docker.service
sudo service docker restart
# if you have a firewall:
sudo ufw allow in from 172.88.88.0/16
```

## Run Standard Containers
### Cleanup
Remove already running containers
```bash
docker container rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
docker container rm -f messenger db keystone consul 2>/dev/null
```


### Internal Network Creation
Create an internal Docker network called `moon`
```bash
docker network create -d bridge --subnet=172.88.88.0/16 --gateway=172.88.88.1 moon
```


### MySql
Run the standard `MySql` container in the `moon` network
```bash
docker container run -dti --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest
```

### Rabbitmq
Run the standard `Rabbitmq` container in the `moon` network
```bash
docker container run -dti --net=moon --hostname messenger --name messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -e RABBITMQ_HIPE_COMPILE=1 -p 5671:5671 -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```


### moon_keystone
Run the `keystone` container (created by the `Moon` project) in the `moon` network
```bash
docker container run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 wukongsun/moon_keystone:ocata
```

### Consul
Run the standard `Consul` container in the `moon` network
```bash
docker run -d --net=moon --name=consul --hostname=consul -p 8500:8500 consul
```


## Run Moon's Containers
### Automatic Launch
To start the `Moon` framework, you only have to run the `moon_orchestrator` container
```bash
docker container run -dti --net moon --hostname orchestrator --name orchestrator wukongsun/moon_orchestrator:v4.1
```


### Manuel Launch 
We can also manually start the `Moon` framework

#### moon_router
```bash
docker container run -dti --net moon --hostname router --name router wukongsun/moon_router:v4.1
```

#### moon_manager
```bash
docker container run -dti --net moon --hostname manager --name manager wukongsun/moon_manager:v4.1
```

#### moon_interface
```bash
docker container run -dti --net moon --hostname interface --name interface wukongsun/moon_interface:v4.1
```

#### moon_orchestrator
```bash
docker container run -dti --net moon --hostname orchestrator --name orchestrator wukongsun/moon_orchestrator:v4.1
```


### Tests
```bash
docker exec -ti interface /bin/bash
pip3 install pytest
cd /usr/local/lib/python3.5/dist-packages/moon_interface/tests/apitests
pytest
```

## Log
### Get some logs
```bash
docker container ps
docker logs db
docker logs messenger
docker logs keystone
docker logs router
docker logs manager
docker logs interface
```
