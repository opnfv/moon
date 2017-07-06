#!/usr/bin/env bash

HOST=

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py

if [ -n "$HOST" ]; then
    RESULT_DIR=${MOON_HOME}/tests/01_smpolicy_average_latency/${HOST}/10
    ARGS="--host=${HOST} --limit=100 -t";
else
    RESULT_DIR=${MOON_HOME}/tests/01_smpolicy_average_latency/localhost/10
    ARGS="--limit=100 -t";
fi
CPT="01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20"

mkdir -p ${RESULT_DIR} 2>/dev/null
#mv ${RESULT_DIR}/docker_stats.rst ${RESULT_DIR}/docker_stats.rst.bak  2>/dev/null

#for SC_INDEX in 01 02 03 04 05 06 07 08 09 10;
for SC_INDEX in 01;
do
    SC=scenario/10/rbac_10_tenant_${SC_INDEX}.py
    echo "Testing ${SC}"
    FILE=${SC##*/}
    FILE=${FILE%.py}
    echo "Testing ${FILE}" >> ${RESULT_DIR}/docker_stats.rst
    echo "===========================" >> ${RESULT_DIR}/docker_stats.rst
    echo "" >> ${RESULT_DIR}/docker_stats.rst
    python3 ${POPULATE_SCRIPT} ${SC}
    for cpt in ${CPT};
    do
        python3 ${TEST_SCRIPT} ${ARGS} --request-per-second ${cpt} --write="${RESULT_DIR}/data_${FILE}_$cpt.json" ${SC}
    done
    #if [ -n "$HOST" ]; then
    #    ssh $HOST docker stats --no-stream --format \"table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.PIDs}}\" >> ${RESULT_DIR}/docker_stats.rst;
    #else
    #    docker stats --no-stream --format "table {{.Name}},{{.CPUPerc}},{{.MemUsage}},{{.PIDs}}" >> ${RESULT_DIR}/docker_stats.rst;
    #fi
    #echo "" >> ${RESULT_DIR}/docker_stats.rst
done

