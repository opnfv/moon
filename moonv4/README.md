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

## Launch MySql, RabbitMQ, Keystone containers
TODO: put all the containers to `dockerhub`
### moon_mysql:v4.1

### moon_rabbitmq:v4.1

### moon_keystone:v4.1
```bash
docker container run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 asteroide/keystone_mitaka:latest
```

## Install Orchestrator
### Get the code

```bash
git clone https://git.opnfv.org/moon
cd moon/moonv4
export MOON_HOME=$(pwd)
sudo ln -s $(pwd)/conf /etc/moon
```

### Start Orchestrator
To start the Moon platform, you have to run the Orchestrator.

TODO: put all Python packages to PIP

```bash
cd ${MOON_HOME}/moon_orchestrator
sudo apt install python3-venv
pyvenv tests/venv
. tests/venv/bin/activate
pip3 install -r requirements.txt --upgrade
pip3 install dist/moon_db-0.1.0.tar.gz --upgrade
pip3 install dist/moon_utilities-0.1.0.tar.gz --upgrade
pip3 install .  --upgrade
moon_db_manager upgrade
```

### `/etc/moon/moon.conf`
- edit `dist_dir` variable
- check each `container` variable 

Launch `Moon Orchestrator`
```bash
moon_orchestrator
```

### Tests
In the Python venv 
```bash
pip3 install pytest
cd ${MOON_HOME}/moon_interface/tests/apitests
pytest
```

## Log
### Get some logs
```bash
docker ps
docker logs messenger
docker logs keystone
docker logs moon_router
docker logs moon_interface
```
