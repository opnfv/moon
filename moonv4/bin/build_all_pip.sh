#!/usr/bin/env bash


echo Building Moon_DB
cd $MOON_HOME/moon_db
python3 setup.py sdist bdist_wheel> /tmp/moon_db.log


echo Building Moon_Utilities
cd $MOON_HOME/moon_utilities
python3 setup.py sdist bdist_wheel> /tmp/moon_utilities.log


echo Building Moon_Orchestrator
cd $MOON_HOME/moon_orchestrator
python3 setup.py sdist bdist_wheel> /tmp/moon_orchestrator.log