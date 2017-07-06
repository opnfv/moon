#!/usr/bin/env bash

HOST=varuna

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py

RESULT_DIR=${MOON_HOME}/tests/21_slave_scalability/${HOST}
ARGS="--host=127.0.0.1 --port=38100 --limit=100 -t";

mkdir -p ${RESULT_DIR} 2>/dev/null

CPT="01 02 03 04 05 06 07 08 09 10"

SC=scenario/10/rbac_10_tenant_01.py
python3 ${POPULATE_SCRIPT} ${SC}

for REQ in 01 02 03 04 05 06 07 08 09 10;
do
    python3 ${TEST_SCRIPT} ${ARGS} --pdp pdp01 --request-per-second ${REQ} --write="${RESULT_DIR}/data_master_${REQ}.json" ${SC}

    ARGS="--host=127.0.0.1 --port=38101 --limit=100 -t";
    python3 ${TEST_SCRIPT} ${ARGS} --pdp pdp01 --request-per-second ${REQ} --write="${RESULT_DIR}/data_slave_${REQ}.json" ${SC}
done

