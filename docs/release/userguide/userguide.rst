Moon Version 4
==============

This directory contains all the modules for MoonV4

Installation
------------

Prerequisite
~~~~~~~~~~~~

    sudo apt install python3-dev python3-pip
    sudo pip3 install pip --upgrade
    sudo apt -y install docker-engine # ([Get Docker](https://docs.docker.com/engine/installation/))
    echo 127.0.0.1 messenger db keystone interface manager | sudo tee -a /etc/hosts

Docker Engine Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Before running containers
-------------------------

Cleanup
~~~~~~~

Remove already running containers

    docker container rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
    docker container rm -f messenger db keystone consul 2>/dev/null


Internal Network Creation
~~~~~~~~~~~~~~~~~~~~~~~~~

Create an internal Docker network called `moon`

    docker network create -d bridge --subnet=172.88.88.0/16 --gateway=172.88.88.1 moon

Install Moon_DB
---------------

Install the moon_db library

    sudo pip3 install moon_db

Starting containers manually
----------------------------

MySql
~~~~~

Run the standard `MySql` container in the `moon` network and configure it

    docker container run -dti --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest
    moon_db_manager upgrade

moon_keystone
~~~~~~~~~~~~~

Run the `keystone` container (created by the `Moon` project) in the `moon` network

    docker container run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 wukongsun/moon_keystone:ocata

Consul
~~~~~~

Run the standard `Consul` container in the `moon` network

    docker run -d --net=moon --name=consul --hostname=consul -p 8500:8500 consul

Moon platform
~~~~~~~~~~~~~

    docker container run -dti --net moon --hostname manager --name manager wukongsun/moon_manager:v4.1
    docker container run -dti --net moon --hostname interface --name interface wukongsun/moon_interface:v4.1

Starting containers automatically
---------------------------------

To start the `Moon` framework, you only have to run the `bootstrap` script

    python3 bin/bootstrap.py

The script will ask you to start one or more Moon containers

Tests
~~~~~

    sudo pip3 install pytest
    cd tests
    pytest

Run scenario
~~~~~~~~~~~~

    sudo pip3 install requests
    cd tests
    python3 populate_default_values.py -v scenario/rbac.py
    python3 send_authz.py -v scenario/rbac.py

Log
---

Get some logs
~~~~~~~~~~~~~

    docker container ps
    docker logs db
    docker logs messenger
    docker logs keystone
    docker logs router
    docker logs manager
    docker logs interface
