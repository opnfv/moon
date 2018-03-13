#!/usr/bin/env bash

cd /data
pip3 install -r tests/unit_python/requirements.txt --upgrade
pip3 install .

if [ -f /data/tests/unit_python/run_tests.sh ];
then
    bash /data/tests/unit_python/run_tests.sh;
fi

cd /data/tests/unit_python
pytest --cov  --cov-report term  --cov-report html --cov-report xml .
