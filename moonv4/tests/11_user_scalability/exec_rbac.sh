#!/usr/bin/env bash

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py --host=varuna --limit=100"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py
RESULT_DIR=${MOON_HOME}/tests/11_user_scalability/varuna/01

SCENARIO_RBAC_10=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_10.py
SCENARIO_RBAC_20=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_20.py
SCENARIO_RBAC_30=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_30.py
SCENARIO_RBAC_40=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_40.py
SCENARIO_RBAC_50=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_50.py
SCENARIO_RBAC_100=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_100.py
SCENARIO_RBAC_250=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_250.py
SCENARIO_RBAC_500=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_500.py
SCENARIO_RBAC_750=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_750.py
SCENARIO_RBAC_1000=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_1000.py
SCENARIO_RBAC_1500=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_1500.py

SCENARIO_SESSION_10=${MOON_HOME}/tests/11_user_scalability/scenario/session_10.py
SCENARIO_SESSION_50=${MOON_HOME}/tests/11_user_scalability/scenario/session_50.py
SCENARIO_SESSION_100=${MOON_HOME}/tests/11_user_scalability/scenario/session_100.py
SCENARIO_SESSION_150=${MOON_HOME}/tests/11_user_scalability/scenario/session_150.py
SCENARIO_SESSION_200=${MOON_HOME}/tests/11_user_scalability/scenario/session_200.py
SCENARIO_SESSION_250=${MOON_HOME}/tests/11_user_scalability/scenario/session_250.py
SCENARIO_SESSION_300=${MOON_HOME}/tests/11_user_scalability/scenario/session_300.py
SCENARIO_SESSION_500=${MOON_HOME}/tests/11_user_scalability/scenario/session_500.py
SCENARIO_SESSION_750=${MOON_HOME}/tests/11_user_scalability/scenario/session_750.py
SCENARIO_SESSION_1000=${MOON_HOME}/tests/11_user_scalability/scenario/session_1000.py
SCENARIO_SESSION_1500=${MOON_HOME}/tests/11_user_scalability/scenario/session_1500.py

mkdir -p ${RESULT_DIR} 2>/dev/null

NUMBER=10

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_10}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_10}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_10}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_10}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_10}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_10}
echo "====================================================="

NUMBER=20

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_20}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_20}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_20}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_20}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_20}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_20}
echo "====================================================="

NUMBER=30

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_30}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_30}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_30}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_30}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_30}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_30}
echo "====================================================="

NUMBER=40

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_40}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_40}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_40}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_40}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_40}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_40}
echo "====================================================="

NUMBER=50

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_50}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_50}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_50}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_50}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_50}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_50}
echo "====================================================="

NUMBER=100

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_100}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_100}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_100}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_100}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_100}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_100}
echo "====================================================="

NUMBER=250

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_250}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_250}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_250}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_250}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_250}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_250}
echo "====================================================="

NUMBER=500

#python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_500}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_500}
echo "====================================================="

NUMBER=750

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_750}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_750}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_750}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_750}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_750}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_750}
echo "====================================================="

NUMBER=1000

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_1000}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_1000}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_1000}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_1000}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_1000}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_1000}
echo "====================================================="

NUMBER=1500

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_1500}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_1500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_1500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_1500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_1500}
echo "====================================================="
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_1500}
echo "====================================================="
