#!/usr/bin/env bash

HOST_MASTER=varuna
PORT_MASTER=38001
HOST_SLAVE=172.18.0.11
PORT_SLAVE=38001

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py

RESULT_DIR=${MOON_HOME}/tests/02_smpolicy_chaining_overhead/${HOST_MASTER}
ARGS="--limit=100 -t";

mkdir -p ${RESULT_DIR} 2>/dev/null

CPT="01 02 03 04 05 06 07 08 09 10"

SC=rbac_10.py
python3 ${POPULATE_SCRIPT} ${SC}

#for REQ in 01 02 03 04 05 06 07 08 09 10;
#do

python3 ${TEST_SCRIPT} --host=${HOST_MASTER} --port=${PORT_SLAVE} ${ARGS} \
    --pdp pdp01 --request-per-second 5 --write="${RESULT_DIR}/data_rbac_05_01.json" ${SC}

#done

echo Press enter to continue
read A

SC=session_10.py
python3 ${POPULATE_SCRIPT} ${SC}

#for REQ in 01 02 03 04 05 06 07 08 09 10;
#do

echo Press enter to continue
read A

python3 ${TEST_SCRIPT} --host=${HOST_MASTER} --port=${PORT_SLAVE} ${ARGS} \
    --pdp pdp01 --request-per-second 5 --write="${RESULT_DIR}/data_rbac_session_05_01.json" ${SC}

#done

