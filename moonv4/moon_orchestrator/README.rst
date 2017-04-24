================================
Core module for the Moon project
================================

This package contains the main module for the Moon project
It is designed to provide the main entry point for the Moon platform.

For any other information, refer to the parent project:

    https://git.opnfv.org/moon


Usage
=====

Get the code
------------

    git clone https://git.opnfv.org/moon
    cd moon
    MOON_HOME=$(pwd)

Create an initial docker
------------------------

    cd /tmp
    git clone https://github.com/rebirthmonkey/vmspace.git
    cd docker/ubuntu_python
    # Check the proxy settings in Dockerfile
    docker build ubuntu:python .

Configure the network
---------------------

    docker network create -d bridge --subnet=172.18.0.0/16 --gateway=172.18.0.1 moon
    echo "127.0.0.1 messenger db" | sudo tee -a /etc/hosts

Start Rabbitmq
--------------

    docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management

Start MySQL server
------------------

    docker run -dti  --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=password -p 3306:3306 mysql:8
    cd $(MOON_HOME)/moon_orchestrator
    mysql -h db -uroot -ppassword < bin/init_db.sql

Get python packages for all components
--------------------------------------

    cd $(MOON_HOME)/moon_orchestrator
    bash bin/build_all.sh
    mysql -h db -uroot -ppassword < bin/init_db.sql

Start Orchestrator
------------------

    cd $(MOON_HOME)/moon_orchestrator
    pyvenv tests/venv
    . tests/venv/bin/activate
    pip install -r ../moon_db/requirements.txt
    pip install -r ../moon_utilities/requirements.txt
    pip install -r requirements.txt
    pip install dist/moon_db-0.1.0.tar.gz
    pip install dist/moon_utilities-0.1.0.tar.gz
    pip install .
    # Check the proxy settings in $(MOON_HOME)/moon_orchestrator/conf/moon.conf
    moon_orchestrator

Get some logs
-------------

    docker logs messenger
    docker logs router
    docker logs interface

Get the API in PDF
------------------

    cd $(MOON_HOME)/moon_interface/tools
    sudo pip install requests
    sudo apt-get install pandoc
    /usr/bin/python3 api2rst.py
    pandoc api.rst -o api.pdf
    evince api.pdf

How to hack the Moon platform
=============================

Update the moon_interface
-------------------------

Go to the directory $(MOON_HOME)/moon_interface and update the code accordingly to your needs,
then update the python package.

    python setup.py sdist
    cp dist/moon_interface_* ../moon_orchestrator/dist
    # kill moon_orchestrator if needed and restart it

Update the moon_secrouter
-------------------------

Go to the directory $(MOON_HOME)/moon_secrouter and update the code accordingly to your needs,
then update the python package.

    python setup.py sdist
    cp dist/moon_secrouter* ../moon_orchestrator/dist
    # kill moon_orchestrator if needed and restart it

Problems that may arise
=======================

If the moon_orchestrator doesn't want to start
(with, for example, the following error: `docker.errors.APIError: 409 Client Error: Conflict`),
check if the router and interface containers still exist and kill and delete them:

    docker kill interface
    docker kill router
    docker rm interface
    docker rm router

If the moon_orchestrator complains that it cannot request the RabbitMQ server,
check if the messenger server is up and running:

    docker ps
    # you must see the messenger running here
    # if not, restart it
    docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
