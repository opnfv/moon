#!/usr/bin/env bash


mkdir $MOON_HOME/moon_orchestrator/dist 2>/dev/null

echo Building Moon_Interface
cd $MOON_HOME/moon_interface
python3 setup.py sdist > /tmp/moon_interface.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_Security_Router
cd $MOON_HOME/moon_secrouter
python3 setup.py sdist > /tmp/moon_secrouter.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_Manager
cd $MOON_HOME/moon_manager
python3 setup.py sdist > /tmp/moon_manager.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_Security_Function
cd $MOON_HOME/moon_secfunction
python3 setup.py sdist > /tmp/moon_secfunction.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_DB
cd $MOON_HOME/moon_db
python3 setup.py sdist > /tmp/moon_db.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_Utilities
cd $MOON_HOME/moon_utilities
python3 setup.py sdist > /tmp/moon_utilities.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist

echo Building Moon_Authz
cd $MOON_HOME/moon_authz
python3 setup.py sdist > /tmp/moon_authz.log
mv dist/*.tar.gz $MOON_HOME/moon_orchestrator/dist
