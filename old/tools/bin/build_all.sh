#!/usr/bin/env bash

VERSION=v4.1
export DOCKER_HOST=tcp://172.88.88.1:2376


mkdir $MOON_HOME/moon_orchestrator/dist 2>/dev/null

echo Building Moon_Orchestrator
cd $MOON_HOME/moon_orchestrator
docker build -t wukongsun/moon_orchestrator:${VERSION} .

echo Building Moon_Interface
cd $MOON_HOME/moon_interface
docker build -t wukongsun/moon_interface:${VERSION} .

echo Building Moon_Security_Router
cd $MOON_HOME/moon_secrouter
docker build -t wukongsun/moon_router:${VERSION} .

echo Building Moon_Manager
cd $MOON_HOME/moon_manager
docker build -t wukongsun/moon_manager:${VERSION} .

echo Building Moon_Authz
cd $MOON_HOME/moon_authz
docker build -t wukongsun/moon_authz:${VERSION} .


echo Building Moon_DB
cd $MOON_HOME/moon_db
python3 setup.py sdist bdist_wheel > /tmp/moon_db.log

echo Building Moon_Utilities
cd $MOON_HOME/moon_utilities
python3 setup.py sdist bdist_wheel > /tmp/moon_utilities.log
