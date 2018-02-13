#!/usr/bin/env bash

echo "Running functional tests :"

#ls -l /data
ls -l /data/tests

if [ -f /data/tests/functional_pod/run_functional_tests.sh ];
then
    echo "running script..."
    bash /data/tests/functional_pod/run_functional_tests.sh;
fi

echo "<END OF JOB>"

