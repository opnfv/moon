#!/usr/bin/env bash

TEST_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/set_authz.py
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py
RESULT_DIR=${MOON_HOME}/tests/11_user_scalability/10_users_rbac
SCENARIO_RBAC=${MOON_HOME}/tests/11_user_scalability/rbac_10.py
SCENARIO_RBAC2=${MOON_HOME}/tests/11_user_scalability/rbac_20.py
SCENARIO_RBAC3=${MOON_HOME}/tests/11_user_scalability/rbac_30.py
SCENARIO_RBAC4=${MOON_HOME}/tests/11_user_scalability/rbac_40.py
SCENARIO_RBAC5=${MOON_HOME}/tests/11_user_scalability/rbac_50.py
SCENARIO_SESSION=${MOON_HOME}/tests/11_user_scalability/session_10.py
SCENARIO_SESSION2=${MOON_HOME}/tests/11_user_scalability/session_20.py
SCENARIO_SESSION3=${MOON_HOME}/tests/11_user_scalability/session_30.py
SCENARIO_SESSION4=${MOON_HOME}/tests/11_user_scalability/session_40.py
SCENARIO_SESSION5=${MOON_HOME}/tests/11_user_scalability/session_50.py

mkdir -p ${RESULT_DIR} 2>/dev/null

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC}
python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_1_1.json" --write-html="${RESULT_DIR}/data_rbac_1_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_1_2.json" --write-html="${RESULT_DIR}/data_rbac_1_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_1_3.json" --write-html="${RESULT_DIR}/data_rbac_1_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_1_4.json" --write-html="${RESULT_DIR}/data_rbac_1_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_1_5.json" --write-html="${RESULT_DIR}/data_rbac_1_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_1_6.json" --write-html="${RESULT_DIR}/data_rbac_1_6.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_1_7.json" --write-html="${RESULT_DIR}/data_rbac_1_7.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_1_8.json" --write-html="${RESULT_DIR}/data_rbac_1_8.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_1_9.json" --write-html="${RESULT_DIR}/data_rbac_1_9.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_1_10.json" --write-html="${RESULT_DIR}/data_rbac_1_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_1_11.json" --write-html="${RESULT_DIR}/data_rbac_1_11.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_1_12.json" --write-html="${RESULT_DIR}/data_rbac_1_12.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_1_13.json" --write-html="${RESULT_DIR}/data_rbac_1_13.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_1_14.json" --write-html="${RESULT_DIR}/data_rbac_1_14.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_1_15.json" --write-html="${RESULT_DIR}/data_rbac_1_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_1_16.json" --write-html="${RESULT_DIR}/data_rbac_1_16.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_1_17.json" --write-html="${RESULT_DIR}/data_rbac_1_17.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_1_18.json" --write-html="${RESULT_DIR}/data_rbac_1_18.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_1_19.json" --write-html="${RESULT_DIR}/data_rbac_1_19.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_1_20.json" --write-html="${RESULT_DIR}/data_rbac_1_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_1_21.json" --write-html="${RESULT_DIR}/data_rbac_1_21.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_1_22.json" --write-html="${RESULT_DIR}/data_rbac_1_22.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_1_23.json" --write-html="${RESULT_DIR}/data_rbac_1_23.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_1_24.json" --write-html="${RESULT_DIR}/data_rbac_1_24.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_1_25.json" --write-html="${RESULT_DIR}/data_rbac_1_25.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_1_26.json" --write-html="${RESULT_DIR}/data_rbac_1_26.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_1_27.json" --write-html="${RESULT_DIR}/data_rbac_1_27.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_1_28.json" --write-html="${RESULT_DIR}/data_rbac_1_28.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_1_29.json" --write-html="${RESULT_DIR}/data_rbac_1_29.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_1_30.json" --write-html="${RESULT_DIR}/data_rbac_1_30.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_1_31.json" --write-html="${RESULT_DIR}/data_rbac_1_31.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_1_32.json" --write-html="${RESULT_DIR}/data_rbac_1_32.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_1_33.json" --write-html="${RESULT_DIR}/data_rbac_1_33.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_1_34.json" --write-html="${RESULT_DIR}/data_rbac_1_34.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_1_35.json" --write-html="${RESULT_DIR}/data_rbac_1_35.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_1_36.json" --write-html="${RESULT_DIR}/data_rbac_1_36.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_1_37.json" --write-html="${RESULT_DIR}/data_rbac_1_37.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_1_38.json" --write-html="${RESULT_DIR}/data_rbac_1_38.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_1_39.json" --write-html="${RESULT_DIR}/data_rbac_1_39.html" ${SCENARIO_RBAC}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC2}
python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION2}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_2_1.json" --write-html="${RESULT_DIR}/data_rbac_2_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_2_2.json" --write-html="${RESULT_DIR}/data_rbac_2_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_2_3.json" --write-html="${RESULT_DIR}/data_rbac_2_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_2_4.json" --write-html="${RESULT_DIR}/data_rbac_2_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_2_5.json" --write-html="${RESULT_DIR}/data_rbac_2_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_2_6.json" --write-html="${RESULT_DIR}/data_rbac_2_6.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_2_7.json" --write-html="${RESULT_DIR}/data_rbac_2_7.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_2_8.json" --write-html="${RESULT_DIR}/data_rbac_2_8.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_2_9.json" --write-html="${RESULT_DIR}/data_rbac_2_9.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_2_10.json" --write-html="${RESULT_DIR}/data_rbac_2_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_2_11.json" --write-html="${RESULT_DIR}/data_rbac_2_11.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_2_12.json" --write-html="${RESULT_DIR}/data_rbac_2_12.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_2_13.json" --write-html="${RESULT_DIR}/data_rbac_2_13.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_2_14.json" --write-html="${RESULT_DIR}/data_rbac_2_14.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_2_15.json" --write-html="${RESULT_DIR}/data_rbac_2_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_2_16.json" --write-html="${RESULT_DIR}/data_rbac_2_16.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_2_17.json" --write-html="${RESULT_DIR}/data_rbac_2_17.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_2_18.json" --write-html="${RESULT_DIR}/data_rbac_2_18.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_2_19.json" --write-html="${RESULT_DIR}/data_rbac_2_19.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_2_20.json" --write-html="${RESULT_DIR}/data_rbac_2_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_2_21.json" --write-html="${RESULT_DIR}/data_rbac_2_21.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_2_22.json" --write-html="${RESULT_DIR}/data_rbac_2_22.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_2_23.json" --write-html="${RESULT_DIR}/data_rbac_2_23.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_2_24.json" --write-html="${RESULT_DIR}/data_rbac_2_24.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_2_25.json" --write-html="${RESULT_DIR}/data_rbac_2_25.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_2_26.json" --write-html="${RESULT_DIR}/data_rbac_2_26.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_2_27.json" --write-html="${RESULT_DIR}/data_rbac_2_27.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_2_28.json" --write-html="${RESULT_DIR}/data_rbac_2_28.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_2_29.json" --write-html="${RESULT_DIR}/data_rbac_2_29.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_2_30.json" --write-html="${RESULT_DIR}/data_rbac_2_30.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_2_31.json" --write-html="${RESULT_DIR}/data_rbac_2_31.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_2_32.json" --write-html="${RESULT_DIR}/data_rbac_2_32.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_2_33.json" --write-html="${RESULT_DIR}/data_rbac_2_33.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_2_34.json" --write-html="${RESULT_DIR}/data_rbac_2_34.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_2_35.json" --write-html="${RESULT_DIR}/data_rbac_2_35.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_2_36.json" --write-html="${RESULT_DIR}/data_rbac_2_36.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_2_37.json" --write-html="${RESULT_DIR}/data_rbac_2_37.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_2_38.json" --write-html="${RESULT_DIR}/data_rbac_2_38.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_2_39.json" --write-html="${RESULT_DIR}/data_rbac_2_39.html" ${SCENARIO_RBAC}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC3}
python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION3}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_3_1.json" --write-html="${RESULT_DIR}/data_rbac_3_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_3_2.json" --write-html="${RESULT_DIR}/data_rbac_3_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_3_3.json" --write-html="${RESULT_DIR}/data_rbac_3_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_3_4.json" --write-html="${RESULT_DIR}/data_rbac_3_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_3_5.json" --write-html="${RESULT_DIR}/data_rbac_3_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_3_6.json" --write-html="${RESULT_DIR}/data_rbac_3_6.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_3_7.json" --write-html="${RESULT_DIR}/data_rbac_3_7.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_3_8.json" --write-html="${RESULT_DIR}/data_rbac_3_8.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_3_9.json" --write-html="${RESULT_DIR}/data_rbac_3_9.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_3_10.json" --write-html="${RESULT_DIR}/data_rbac_3_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_3_11.json" --write-html="${RESULT_DIR}/data_rbac_3_11.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_3_12.json" --write-html="${RESULT_DIR}/data_rbac_3_12.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_3_13.json" --write-html="${RESULT_DIR}/data_rbac_3_13.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_3_14.json" --write-html="${RESULT_DIR}/data_rbac_3_14.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_3_15.json" --write-html="${RESULT_DIR}/data_rbac_3_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_3_16.json" --write-html="${RESULT_DIR}/data_rbac_3_16.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_3_17.json" --write-html="${RESULT_DIR}/data_rbac_3_17.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_3_18.json" --write-html="${RESULT_DIR}/data_rbac_3_18.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_3_19.json" --write-html="${RESULT_DIR}/data_rbac_3_19.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_3_20.json" --write-html="${RESULT_DIR}/data_rbac_3_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_3_21.json" --write-html="${RESULT_DIR}/data_rbac_3_21.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_3_22.json" --write-html="${RESULT_DIR}/data_rbac_3_22.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_3_23.json" --write-html="${RESULT_DIR}/data_rbac_3_23.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_3_24.json" --write-html="${RESULT_DIR}/data_rbac_3_24.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_3_25.json" --write-html="${RESULT_DIR}/data_rbac_3_25.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_3_26.json" --write-html="${RESULT_DIR}/data_rbac_3_26.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_3_27.json" --write-html="${RESULT_DIR}/data_rbac_3_27.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_3_28.json" --write-html="${RESULT_DIR}/data_rbac_3_28.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_3_29.json" --write-html="${RESULT_DIR}/data_rbac_3_29.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_3_30.json" --write-html="${RESULT_DIR}/data_rbac_3_30.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_3_31.json" --write-html="${RESULT_DIR}/data_rbac_3_31.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_3_32.json" --write-html="${RESULT_DIR}/data_rbac_3_32.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_3_33.json" --write-html="${RESULT_DIR}/data_rbac_3_33.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_3_34.json" --write-html="${RESULT_DIR}/data_rbac_3_34.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_3_35.json" --write-html="${RESULT_DIR}/data_rbac_3_35.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_3_36.json" --write-html="${RESULT_DIR}/data_rbac_3_36.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_3_37.json" --write-html="${RESULT_DIR}/data_rbac_3_37.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_3_38.json" --write-html="${RESULT_DIR}/data_rbac_3_38.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_3_39.json" --write-html="${RESULT_DIR}/data_rbac_3_39.html" ${SCENARIO_RBAC}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC4}
python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION4}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_4_1.json" --write-html="${RESULT_DIR}/data_rbac_4_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_4_2.json" --write-html="${RESULT_DIR}/data_rbac_4_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_4_3.json" --write-html="${RESULT_DIR}/data_rbac_4_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_4_4.json" --write-html="${RESULT_DIR}/data_rbac_4_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_4_5.json" --write-html="${RESULT_DIR}/data_rbac_4_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_4_6.json" --write-html="${RESULT_DIR}/data_rbac_4_6.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_4_7.json" --write-html="${RESULT_DIR}/data_rbac_4_7.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_4_8.json" --write-html="${RESULT_DIR}/data_rbac_4_8.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_4_9.json" --write-html="${RESULT_DIR}/data_rbac_4_9.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_4_10.json" --write-html="${RESULT_DIR}/data_rbac_4_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_4_11.json" --write-html="${RESULT_DIR}/data_rbac_4_11.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_4_12.json" --write-html="${RESULT_DIR}/data_rbac_4_12.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_4_13.json" --write-html="${RESULT_DIR}/data_rbac_4_13.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_4_14.json" --write-html="${RESULT_DIR}/data_rbac_4_14.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_4_15.json" --write-html="${RESULT_DIR}/data_rbac_4_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_4_16.json" --write-html="${RESULT_DIR}/data_rbac_4_16.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_4_17.json" --write-html="${RESULT_DIR}/data_rbac_4_17.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_4_18.json" --write-html="${RESULT_DIR}/data_rbac_4_18.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_4_19.json" --write-html="${RESULT_DIR}/data_rbac_4_19.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_4_20.json" --write-html="${RESULT_DIR}/data_rbac_4_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_4_21.json" --write-html="${RESULT_DIR}/data_rbac_4_21.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_4_22.json" --write-html="${RESULT_DIR}/data_rbac_4_22.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_4_23.json" --write-html="${RESULT_DIR}/data_rbac_4_23.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_4_24.json" --write-html="${RESULT_DIR}/data_rbac_4_24.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_4_25.json" --write-html="${RESULT_DIR}/data_rbac_4_25.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_4_26.json" --write-html="${RESULT_DIR}/data_rbac_4_26.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_4_27.json" --write-html="${RESULT_DIR}/data_rbac_4_27.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_4_28.json" --write-html="${RESULT_DIR}/data_rbac_4_28.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_4_29.json" --write-html="${RESULT_DIR}/data_rbac_4_29.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_4_30.json" --write-html="${RESULT_DIR}/data_rbac_4_30.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_4_31.json" --write-html="${RESULT_DIR}/data_rbac_4_31.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_4_32.json" --write-html="${RESULT_DIR}/data_rbac_4_32.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_4_33.json" --write-html="${RESULT_DIR}/data_rbac_4_33.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_4_34.json" --write-html="${RESULT_DIR}/data_rbac_4_34.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_4_35.json" --write-html="${RESULT_DIR}/data_rbac_4_35.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_4_36.json" --write-html="${RESULT_DIR}/data_rbac_4_36.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_4_37.json" --write-html="${RESULT_DIR}/data_rbac_4_37.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_4_38.json" --write-html="${RESULT_DIR}/data_rbac_4_38.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_4_39.json" --write-html="${RESULT_DIR}/data_rbac_4_39.html" ${SCENARIO_RBAC}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC5}
python3 ${POPULATE_SCRIPT} ${SCENARIO_SESSION5}

python3 ${TEST_SCRIPT} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_5_1.json" --write-html="${RESULT_DIR}/data_rbac_5_1.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_5_2.json" --write-html="${RESULT_DIR}/data_rbac_5_2.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_5_3.json" --write-html="${RESULT_DIR}/data_rbac_5_3.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_5_4.json" --write-html="${RESULT_DIR}/data_rbac_5_4.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_5_5.json" --write-html="${RESULT_DIR}/data_rbac_5_5.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_5_6.json" --write-html="${RESULT_DIR}/data_rbac_5_6.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_5_7.json" --write-html="${RESULT_DIR}/data_rbac_5_7.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_5_8.json" --write-html="${RESULT_DIR}/data_rbac_5_8.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_5_9.json" --write-html="${RESULT_DIR}/data_rbac_5_9.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_5_10.json" --write-html="${RESULT_DIR}/data_rbac_5_10.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_5_11.json" --write-html="${RESULT_DIR}/data_rbac_5_11.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_5_12.json" --write-html="${RESULT_DIR}/data_rbac_5_12.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_5_13.json" --write-html="${RESULT_DIR}/data_rbac_5_13.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_5_14.json" --write-html="${RESULT_DIR}/data_rbac_5_14.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_5_15.json" --write-html="${RESULT_DIR}/data_rbac_5_15.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_5_16.json" --write-html="${RESULT_DIR}/data_rbac_5_16.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_5_17.json" --write-html="${RESULT_DIR}/data_rbac_5_17.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_5_18.json" --write-html="${RESULT_DIR}/data_rbac_5_18.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_5_19.json" --write-html="${RESULT_DIR}/data_rbac_5_19.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_5_20.json" --write-html="${RESULT_DIR}/data_rbac_5_20.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 21 --write="${RESULT_DIR}/data_rbac_5_21.json" --write-html="${RESULT_DIR}/data_rbac_5_21.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 22 --write="${RESULT_DIR}/data_rbac_5_22.json" --write-html="${RESULT_DIR}/data_rbac_5_22.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 23 --write="${RESULT_DIR}/data_rbac_5_23.json" --write-html="${RESULT_DIR}/data_rbac_5_23.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 24 --write="${RESULT_DIR}/data_rbac_5_24.json" --write-html="${RESULT_DIR}/data_rbac_5_24.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 25 --write="${RESULT_DIR}/data_rbac_5_25.json" --write-html="${RESULT_DIR}/data_rbac_5_25.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 26 --write="${RESULT_DIR}/data_rbac_5_26.json" --write-html="${RESULT_DIR}/data_rbac_5_26.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 27 --write="${RESULT_DIR}/data_rbac_5_27.json" --write-html="${RESULT_DIR}/data_rbac_5_27.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 28 --write="${RESULT_DIR}/data_rbac_5_28.json" --write-html="${RESULT_DIR}/data_rbac_5_28.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 29 --write="${RESULT_DIR}/data_rbac_5_29.json" --write-html="${RESULT_DIR}/data_rbac_5_29.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 30 --write="${RESULT_DIR}/data_rbac_5_30.json" --write-html="${RESULT_DIR}/data_rbac_5_30.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 31 --write="${RESULT_DIR}/data_rbac_5_31.json" --write-html="${RESULT_DIR}/data_rbac_5_31.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 32 --write="${RESULT_DIR}/data_rbac_5_32.json" --write-html="${RESULT_DIR}/data_rbac_5_32.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 33 --write="${RESULT_DIR}/data_rbac_5_33.json" --write-html="${RESULT_DIR}/data_rbac_5_33.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 34 --write="${RESULT_DIR}/data_rbac_5_34.json" --write-html="${RESULT_DIR}/data_rbac_5_34.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 35 --write="${RESULT_DIR}/data_rbac_5_35.json" --write-html="${RESULT_DIR}/data_rbac_5_35.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 36 --write="${RESULT_DIR}/data_rbac_5_36.json" --write-html="${RESULT_DIR}/data_rbac_5_36.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 37 --write="${RESULT_DIR}/data_rbac_5_37.json" --write-html="${RESULT_DIR}/data_rbac_5_37.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 38 --write="${RESULT_DIR}/data_rbac_5_38.json" --write-html="${RESULT_DIR}/data_rbac_5_38.html" ${SCENARIO_RBAC}
python3 ${TEST_SCRIPT} --request-per-second 39 --write="${RESULT_DIR}/data_rbac_5_39.json" --write-html="${RESULT_DIR}/data_rbac_5_39.html" ${SCENARIO_RBAC}

