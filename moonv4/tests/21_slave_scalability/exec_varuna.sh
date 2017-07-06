#!/usr/bin/env bash

HOST_MASTER=varuna
PORT_MASTER=38001
HOST_SLAVE=172.18.0.11
PORT_SLAVE=38001

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py

RESULT_DIR=${MOON_HOME}/tests/21_slave_scalability/${HOST_MASTER}_${HOST_SLAVE}
ARGS="--limit=100";

mkdir -p ${RESULT_DIR} 2>/dev/null

CPT="01 02 03 04 05 06 07 08 09 10"

SC=scenario/10/rbac_10_tenant_01.py
python3 ${POPULATE_SCRIPT} ${SC}

#cd ${MOON_HOME}

for REQ in 01 02 03 04 05 06 07 08 09 10;
do

#    ${MOON_HOME}/bin/start.sh &
#
#    echo "waiting for Orchestrator..."
#    echo -e "\033[35m"
#    sed '/Starting MQ server with topic: orchestrator/q' <(tail -f /tmp/orchestrator.log)
#    echo -e "\033[m"

    python3 ${TEST_SCRIPT} --host=${HOST_SLAVE} --port=${PORT_SLAVE} ${ARGS} --pdp pdp01 --request-per-second 5 --write="${RESULT_DIR}/data_slave_05_${REQ}.json" ${SC}
#    python3 ../../moon_interface/tests/apitests/plot_json.py latency "${RESULT_DIR}/data_slave_05_${REQ}.json" -w

#    kill $(cat moon_orchestrator.pid)
#
#    echo "waiting for Orchestrator..."
#    echo -e "\033[35m"
#    sed '/Moon orchestrator: offline/q' <(tail -f /tmp/orchestrator.log)
#    echo -e "\033[m"

    echo ================================= Restart Moon =================================
    read A

done

