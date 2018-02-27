#!/usr/bin/env bash

cd /data
#pip3 install -r tests/python_unit/requirements.txt --upgrade
#pip3 install .

if [ -f /data/tests/unit_python/run_tests.sh ];
then
    bash /data/tests/unit_python/run_tests.sh;
fi

cd /data/tests/unit_python
pytest -s .
