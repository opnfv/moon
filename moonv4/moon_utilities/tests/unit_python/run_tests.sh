#!/usr/bin/env bash

cd /data
pip3 install -r tests/unit_python/requirements.txt --upgrade
pip3 install .

cd /data/tests/unit_python
pytest .
