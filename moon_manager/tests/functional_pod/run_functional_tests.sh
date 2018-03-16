#!/usr/bin/env bash

if [ -d /data/dist ];
then
    pip install /data/dist/*.tar.gz --upgrade
    pip install /data/dist/*.whl --upgrade
fi


cd /data/tests/functional_pod
pytest .
