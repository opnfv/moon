#!/usr/bin/env bash

echo "starting Moon Functional Tests"

COMPONENTS="moon_authz, moon_interface, moon_manager, moon_orchestrator, moon_wrapper"

for dir in ${COMPONENTS}; do
    echo "Testing component ${dir}"
    cd ${MOON_HOME}/${dir}
    docker run --rm --volume $(pwd):/data wukongsun/moon_forming:latest /bin/bash /root/switch.sh functest
done

# TODO: download tests results
