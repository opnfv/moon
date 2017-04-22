# Modules for the Moon project

This directory contains all the modules for MoonV4


## Usage

### Prerequist

-   `sudo apt install python3-dev python3-pip`
-   `sudo pip3 install pip --upgrade`
-   `sudo apt -y install docker-engine` ([Get Docker](https://docs.docker.com/engine/installation/))
-   `echo 127.0.0.1 messenger db keystone | sudo tee -a /etc/hosts`
-   modify moon orchestrator dist path in moon_orchestrator/conf/moon.conf
-   `sudo ln -s $(pwd)/conf /etc/moon`

### Get the code

```bash
git clone https://github.com/rebirthmonkey/moonv4.git
cd moonv4
export MOON_HOME=$(pwd)
```

### Create an OpenStack environment

```bash
cd $MOON_HOME/templates/docker/keystone
# Check the proxy settings in Dockerfile
sudo docker build -t keystone:mitaka .
```

### Start RabbitMQ

```bash
sudo docker network create -d bridge --subnet=172.18.0.0/16 --gateway=172.18.0.1 moon
sudo docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
```

### Start MySQL server

```bash
sudo docker run -dti  --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest
```

### Start an OpenStack environment

```bash
sudo docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka
```

### Build python packages for all components

```bash
cd ${MOON_HOME}/moon_orchestrator
sudo pip3 install pip --upgrade
cd ${MOON_HOME}/bin
source build_all.sh
```

### Start Orchestrator

To start the Moon platform, you have to run the Orchestrator.

```bash
cd ${MOON_HOME}/moon_orchestrator
sudo apt-get install python3-venv (or apt-get install -y python3 python-virtualenv on Ubuntu 14.04)
pyvenv tests/venv (or virtualenv tests/venv on Ubuntu 14.04)
. tests/venv/bin/activate
sudo pip3 install -r requirements.txt --upgrade
sudo pip3 install dist/moon_db-0.1.0.tar.gz --upgrade
sudo pip3 install dist/moon_utilities-0.1.0.tar.gz --upgrade
sudo pip3 install .  --upgrade
# Check the proxy settings and edit dist_dir variable  in $(MOON_HOME)/moon_orchestrator/etc/moon.conf
# Adapt the path used in the cd command in $(MOON_HOME)/bin/start.sh
source ../bin/start.sh
```

### Tests
```bash
sudo pip3 install pytest
cd ${MOON_HOME}/moon_interface/tests/apitests
pytest
```


### Relaunch Keystone docker
If error of `get_keystone_projects()`, then relaunch the Keystone docker, and wait 40 seconds!!!
```bash
docker rm -f keystone
docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka
```

### Add default data in DB
Pre-fill the DB with a RBAC policy
```bash
cd ${MOON_HOME}/moon_interface/tests/apitests
python3 populate_default_values.py scenario/ rbac.py
```


### Get some logs

```bash
docker ps
docker logs messenger
docker logs keystone
docker logs moon_router
docker logs moon_interface
```

### Get some statistics

```bash
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.PIDs}}"
```

### Get the API in PDF

```bash
cd ${MOON_HOME}/moon_interface/tools
sudo pip3 install requests
sudo apt-get install pandoc
/usr/bin/python3 api2rst.py
sudo apt-get install texlive-latex-extra
pandoc api.rst -o api.pdf
evince api.pdf
```

## How to hack the Moon platform

### Force the build of components

If you want to rebuild one or more component, you have to modify the configuration file `moon.conf`. 

For example, if you want to rebuild the moon_interface, got to the `[interface]` section and delete the 
value of the container key like this:

```
[interface]
host=172.18.0.11
port=38001
# Name of the container to download (if empty build from scratch)
# example: container=moon/moon_interface:latest
container=
```

You can configure the interface, the router and both the security_function and security_policy.
You can also force the version of the component like this: `container=moon/moon_interface:4.0.0`

### Update the moon_interface

Go to the directory `${MOON_HOME}/moon_interface` and update the code accordingly to your needs,
then update the python package.

```bash
cd ${MOON_HOME}/moon_interface
python setup.py sdist
cp dist/moon_interface_* ../moon_orchestrator/dist
# kill moon_orchestrator if needed and restart it
```

### Update the moon_secrouter

Go to the directory `${MOON_HOME}/moon_secrouter` and update the code accordingly to your needs,
then update the python package.

```bash
cd ${MOON_HOME}/moon_secrouter
python setup.py sdist
cp dist/moon_secrouter* ../moon_orchestrator/dist
# kill moon_orchestrator if needed and restart it
```

## Problems that may arise

If the moon_orchestrator doesn't want to start
(with, for example, the following error: `docker.errors.APIError: 409 Client Error: Conflict`),
check if the router and interface containers still exist and kill and delete them:

```bash
docker kill moon_interface
docker kill moon_router
docker rm moon_interface
docker rm moon_router
```

If the moon_orchestrator complains that it cannot request the RabbitMQ server,
check if the messenger server is up and running:

```bash
docker ps
# you must see the messenger running here
# if not, restart it
docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
```
