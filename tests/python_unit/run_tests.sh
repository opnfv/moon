#!/usr/bin/env bash

cd ${MOON_HOME}/python_moonclient
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest