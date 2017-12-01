#!/usr/bin/env bash

cd /data
pip3 install .

cd /data/tests/unit_python
pytest .
