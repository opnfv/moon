#!/usr/bin/env bash

CMD=$1

echo "COMMAND IS ${CMD}"

if [ "${CMD}" = "functest" ]; then
    echo "FUNCTIONAL TESTS"
    ls -l /data
    ls -l /data/tests
    sh /data/tests/functional_pod/run_functional_tests.sh
#elif [ $CMD == "unittest" ]; then
#    sh /data/tests/functional_pod/run_functional_tests.sh
else
    echo "CONFIGURATION"
    bash config_moon.sh
fi

echo "<END OF JOB>"