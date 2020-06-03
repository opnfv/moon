#!/usr/bin/env bash

MOON_HOME=${1:-.}

echo "Starting Moon Functional Tests on ${MOON_HOME}"

cd ${MOON_HOME}

COMPONENTS="moon_manager moon_wrapper"

for dir in ${COMPONENTS}; do
    echo "Testing component ${dir}"
    cd ${MOON_HOME}/${dir}
    bash ../tests/functional/run_tests_for_component.sh
    cd -
done

# TODO: download tests results
