#!/usr/bin/env bash

TEST_SCRIPT="${MOON_HOME}/moon_interface/tests/apitests/set_authz.py --limit=100 --host=varuna"
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py
RESULT_DIR=${MOON_HOME}/tests/11_user_scalability/results/1500

SCENARIO_RBAC_10=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_10.py
SCENARIO_RBAC_50=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_50.py
SCENARIO_RBAC_100=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_100.py
SCENARIO_RBAC_150=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_150.py
SCENARIO_RBAC_200=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_200.py
SCENARIO_RBAC_250=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_250.py
SCENARIO_RBAC_300=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_300.py
SCENARIO_RBAC_500=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_500.py
SCENARIO_RBAC_750=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_750.py
SCENARIO_RBAC_1000=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_1000.py
SCENARIO_RBAC_1500=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_1500.py
SCENARIO_RBAC_3000=${MOON_HOME}/tests/11_user_scalability/scenario/rbac_3000.py

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

NUMBER=3000

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC_3000}
#python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}_${NUMBER}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_${NUMBER}_01.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_01.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_${NUMBER}_02.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_02.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_${NUMBER}_03.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_03.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_${NUMBER}_04.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_04.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_${NUMBER}_05.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_05.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_${NUMBER}_06.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_06.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_${NUMBER}_07.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_07.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_${NUMBER}_08.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_08.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_${NUMBER}_09.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_09.html" ${SCENARIO_RBAC_1500}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_${NUMBER}_10.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_10.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_${NUMBER}_11.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_11.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_${NUMBER}_12.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_12.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_${NUMBER}_13.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_13.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_${NUMBER}_14.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_14.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_${NUMBER}_15.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_15.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_${NUMBER}_16.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_16.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_${NUMBER}_17.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_17.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_${NUMBER}_18.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_18.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_${NUMBER}_19.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_19.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_${NUMBER}_20.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_20.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_${NUMBER}_21.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_21.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_${NUMBER}_22.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_22.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_${NUMBER}_23.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_23.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_${NUMBER}_24.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_24.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_${NUMBER}_25.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_25.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_${NUMBER}_26.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_26.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_${NUMBER}_27.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_27.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_${NUMBER}_28.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_28.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_${NUMBER}_29.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_29.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_${NUMBER}_30.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_30.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_${NUMBER}_31.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_31.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_${NUMBER}_32.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_32.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_${NUMBER}_33.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_33.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_${NUMBER}_34.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_34.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_${NUMBER}_35.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_35.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_${NUMBER}_36.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_36.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_${NUMBER}_37.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_37.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_${NUMBER}_38.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_38.html" ${SCENARIO_RBAC_1500}
#python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_${NUMBER}_39.json" --write-html="${RESULT_DIR}/data_rbac_${NUMBER}_39.html" ${SCENARIO_RBAC_1500}

