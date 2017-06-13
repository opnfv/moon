#!/usr/bin/env bash

TEST_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/set_authz.py
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py
RESULT_DIR=${MOON_HOME}/tests/02_smpolicy_chaining_overhead/10_users_rbac
SCENARIO_RBAC=${MOON_HOME}/tests/02_smpolicy_chaining_overhead/rbac_10.py
SCENARIO_SESSION=${MOON_HOME}/tests/02_smpolicy_chaining_overhead/session.py

mkdir -p ${RESULT_DIR} 2>/dev/null

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC}
# python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_1.json" --write-html="${RESULT_DIR}/data_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_2.json" --write-html="${RESULT_DIR}/data_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_3.json" --write-html="${RESULT_DIR}/data_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_4.json" --write-html="${RESULT_DIR}/data_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_5.json" --write-html="${RESULT_DIR}/data_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_10.json" --write-html="${RESULT_DIR}/data_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_15.json" --write-html="${RESULT_DIR}/data_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_20.json" --write-html="${RESULT_DIR}/data_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_25.json" --write-html="${RESULT_DIR}/data_25.html" ${SCENARIO_RBAC}
