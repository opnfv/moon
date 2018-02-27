#!/usr/bin/env bash

echo "starting Moon Functional Tests"

cd python_moonutilities
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest

cd ../python_moondb
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest

cd ../python_moonclient
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest

cd ../moon_manager
rm -f tests/unit_python/database.db
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest

