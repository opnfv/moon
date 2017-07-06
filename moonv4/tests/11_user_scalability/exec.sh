#!/usr/bin/env bash

TEST_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/set_authz.py
POPULATE_SCRIPT=${MOON_HOME}/moon_interface/tests/apitests/populate_default_values.py
RESULT_DIR=${MOON_HOME}/tests/01_smpolicy_average_latency/varuna/ida/01
HOST="--host=varuna"

SCENARIO_RBAC010=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_10.py
SCENARIO_RBAC050=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_50.py
SCENARIO_RBAC100=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_100.py
SCENARIO_RBAC150=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_150.py
SCENARIO_RBAC200=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_200.py
SCENARIO_RBAC250=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_250.py
SCENARIO_RBAC300=${MOON_HOME}/tests/01_smpolicy_average_latency/rbac_300.py

SCENARIO_SESSION=${MOON_HOME}/tests/01_smpolicy_average_latency/session.py

mkdir -p ${RESULT_DIR} 2>/dev/null

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC010}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_10_01.json" --write-html="${RESULT_DIR}/data_rbac_10_01.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_10_02.json" --write-html="${RESULT_DIR}/data_rbac_10_02.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_10_03.json" --write-html="${RESULT_DIR}/data_rbac_10_03.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_10_04.json" --write-html="${RESULT_DIR}/data_rbac_10_04.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_10_05.json" --write-html="${RESULT_DIR}/data_rbac_10_05.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_10_06.json" --write-html="${RESULT_DIR}/data_rbac_10_06.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_10_07.json" --write-html="${RESULT_DIR}/data_rbac_10_07.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_10_08.json" --write-html="${RESULT_DIR}/data_rbac_10_08.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_10_09.json" --write-html="${RESULT_DIR}/data_rbac_10_09.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_10_10.json" --write-html="${RESULT_DIR}/data_rbac_10_10.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_10_11.json" --write-html="${RESULT_DIR}/data_rbac_10_11.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_10_12.json" --write-html="${RESULT_DIR}/data_rbac_10_12.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_10_13.json" --write-html="${RESULT_DIR}/data_rbac_10_13.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_10_14.json" --write-html="${RESULT_DIR}/data_rbac_10_14.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_10_15.json" --write-html="${RESULT_DIR}/data_rbac_10_15.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_10_16.json" --write-html="${RESULT_DIR}/data_rbac_10_16.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_10_17.json" --write-html="${RESULT_DIR}/data_rbac_10_17.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_10_18.json" --write-html="${RESULT_DIR}/data_rbac_10_18.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_10_19.json" --write-html="${RESULT_DIR}/data_rbac_10_19.html" ${SCENARIO_RBAC010}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_10_20.json" --write-html="${RESULT_DIR}/data_rbac_10_20.html" ${SCENARIO_RBAC010}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC050}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_50_01.json" --write-html="${RESULT_DIR}/data_rbac_50_01.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_50_02.json" --write-html="${RESULT_DIR}/data_rbac_50_02.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_50_03.json" --write-html="${RESULT_DIR}/data_rbac_50_03.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_50_04.json" --write-html="${RESULT_DIR}/data_rbac_50_04.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_50_05.json" --write-html="${RESULT_DIR}/data_rbac_50_05.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_50_06.json" --write-html="${RESULT_DIR}/data_rbac_50_06.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_50_07.json" --write-html="${RESULT_DIR}/data_rbac_50_07.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_50_08.json" --write-html="${RESULT_DIR}/data_rbac_50_08.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_50_09.json" --write-html="${RESULT_DIR}/data_rbac_50_09.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_50_10.json" --write-html="${RESULT_DIR}/data_rbac_50_10.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_50_11.json" --write-html="${RESULT_DIR}/data_rbac_50_11.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_50_12.json" --write-html="${RESULT_DIR}/data_rbac_50_12.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_50_13.json" --write-html="${RESULT_DIR}/data_rbac_50_13.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_50_14.json" --write-html="${RESULT_DIR}/data_rbac_50_14.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_50_15.json" --write-html="${RESULT_DIR}/data_rbac_50_15.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_50_16.json" --write-html="${RESULT_DIR}/data_rbac_50_16.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_50_17.json" --write-html="${RESULT_DIR}/data_rbac_50_17.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_50_18.json" --write-html="${RESULT_DIR}/data_rbac_50_18.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_50_19.json" --write-html="${RESULT_DIR}/data_rbac_50_19.html" ${SCENARIO_RBAC050}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_50_20.json" --write-html="${RESULT_DIR}/data_rbac_50_20.html" ${SCENARIO_RBAC050}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC100}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_100_01.json" --write-html="${RESULT_DIR}/data_rbac_100_01.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_100_02.json" --write-html="${RESULT_DIR}/data_rbac_100_02.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_100_03.json" --write-html="${RESULT_DIR}/data_rbac_100_03.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_100_04.json" --write-html="${RESULT_DIR}/data_rbac_100_04.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_100_05.json" --write-html="${RESULT_DIR}/data_rbac_100_05.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_100_06.json" --write-html="${RESULT_DIR}/data_rbac_100_06.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_100_07.json" --write-html="${RESULT_DIR}/data_rbac_100_07.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_100_08.json" --write-html="${RESULT_DIR}/data_rbac_100_08.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_100_09.json" --write-html="${RESULT_DIR}/data_rbac_100_09.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_100_10.json" --write-html="${RESULT_DIR}/data_rbac_100_10.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_100_11.json" --write-html="${RESULT_DIR}/data_rbac_100_11.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_100_12.json" --write-html="${RESULT_DIR}/data_rbac_100_12.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_100_13.json" --write-html="${RESULT_DIR}/data_rbac_100_13.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_100_14.json" --write-html="${RESULT_DIR}/data_rbac_100_14.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_100_15.json" --write-html="${RESULT_DIR}/data_rbac_100_15.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_100_16.json" --write-html="${RESULT_DIR}/data_rbac_100_16.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_100_17.json" --write-html="${RESULT_DIR}/data_rbac_100_17.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_100_18.json" --write-html="${RESULT_DIR}/data_rbac_100_18.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_100_19.json" --write-html="${RESULT_DIR}/data_rbac_100_19.html" ${SCENARIO_RBAC100}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_100_20.json" --write-html="${RESULT_DIR}/data_rbac_100_20.html" ${SCENARIO_RBAC100}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC150}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_150_01.json" --write-html="${RESULT_DIR}/data_rbac_150_01.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_150_02.json" --write-html="${RESULT_DIR}/data_rbac_150_02.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_150_03.json" --write-html="${RESULT_DIR}/data_rbac_150_03.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_150_04.json" --write-html="${RESULT_DIR}/data_rbac_150_04.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_150_05.json" --write-html="${RESULT_DIR}/data_rbac_150_05.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_150_06.json" --write-html="${RESULT_DIR}/data_rbac_150_06.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_150_07.json" --write-html="${RESULT_DIR}/data_rbac_150_07.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_150_08.json" --write-html="${RESULT_DIR}/data_rbac_150_08.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_150_09.json" --write-html="${RESULT_DIR}/data_rbac_150_09.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_150_10.json" --write-html="${RESULT_DIR}/data_rbac_150_10.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_150_11.json" --write-html="${RESULT_DIR}/data_rbac_150_11.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_150_12.json" --write-html="${RESULT_DIR}/data_rbac_150_12.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_150_13.json" --write-html="${RESULT_DIR}/data_rbac_150_13.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_150_14.json" --write-html="${RESULT_DIR}/data_rbac_150_14.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_150_15.json" --write-html="${RESULT_DIR}/data_rbac_150_15.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_150_16.json" --write-html="${RESULT_DIR}/data_rbac_150_16.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_150_17.json" --write-html="${RESULT_DIR}/data_rbac_150_17.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_150_18.json" --write-html="${RESULT_DIR}/data_rbac_150_18.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_150_19.json" --write-html="${RESULT_DIR}/data_rbac_150_19.html" ${SCENARIO_RBAC150}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_150_20.json" --write-html="${RESULT_DIR}/data_rbac_100_20.html" ${SCENARIO_RBAC150}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC200}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_200_01.json" --write-html="${RESULT_DIR}/data_rbac_200_01.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_200_02.json" --write-html="${RESULT_DIR}/data_rbac_200_02.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_200_03.json" --write-html="${RESULT_DIR}/data_rbac_200_03.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_200_04.json" --write-html="${RESULT_DIR}/data_rbac_200_04.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_200_05.json" --write-html="${RESULT_DIR}/data_rbac_200_05.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_200_06.json" --write-html="${RESULT_DIR}/data_rbac_200_06.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_200_07.json" --write-html="${RESULT_DIR}/data_rbac_200_07.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_200_08.json" --write-html="${RESULT_DIR}/data_rbac_200_08.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_200_09.json" --write-html="${RESULT_DIR}/data_rbac_200_09.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_200_10.json" --write-html="${RESULT_DIR}/data_rbac_200_10.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_200_11.json" --write-html="${RESULT_DIR}/data_rbac_200_11.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_200_12.json" --write-html="${RESULT_DIR}/data_rbac_200_12.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_200_13.json" --write-html="${RESULT_DIR}/data_rbac_200_13.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_200_14.json" --write-html="${RESULT_DIR}/data_rbac_200_14.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_200_15.json" --write-html="${RESULT_DIR}/data_rbac_200_15.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_200_16.json" --write-html="${RESULT_DIR}/data_rbac_200_16.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_200_17.json" --write-html="${RESULT_DIR}/data_rbac_200_17.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_200_18.json" --write-html="${RESULT_DIR}/data_rbac_200_18.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_200_19.json" --write-html="${RESULT_DIR}/data_rbac_200_19.html" ${SCENARIO_RBAC200}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_200_20.json" --write-html="${RESULT_DIR}/data_rbac_100_20.html" ${SCENARIO_RBAC200}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC250}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_250_01.json" --write-html="${RESULT_DIR}/data_rbac_250_01.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_250_02.json" --write-html="${RESULT_DIR}/data_rbac_250_02.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_250_03.json" --write-html="${RESULT_DIR}/data_rbac_250_03.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_250_04.json" --write-html="${RESULT_DIR}/data_rbac_250_04.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_250_05.json" --write-html="${RESULT_DIR}/data_rbac_250_05.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_250_06.json" --write-html="${RESULT_DIR}/data_rbac_250_06.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_250_07.json" --write-html="${RESULT_DIR}/data_rbac_250_07.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_250_08.json" --write-html="${RESULT_DIR}/data_rbac_250_08.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_250_09.json" --write-html="${RESULT_DIR}/data_rbac_250_09.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_250_10.json" --write-html="${RESULT_DIR}/data_rbac_250_10.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_250_11.json" --write-html="${RESULT_DIR}/data_rbac_250_11.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_250_12.json" --write-html="${RESULT_DIR}/data_rbac_250_12.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_250_13.json" --write-html="${RESULT_DIR}/data_rbac_250_13.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_250_14.json" --write-html="${RESULT_DIR}/data_rbac_250_14.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_250_15.json" --write-html="${RESULT_DIR}/data_rbac_250_15.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_250_16.json" --write-html="${RESULT_DIR}/data_rbac_250_16.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_250_17.json" --write-html="${RESULT_DIR}/data_rbac_250_17.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_250_18.json" --write-html="${RESULT_DIR}/data_rbac_250_18.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_250_19.json" --write-html="${RESULT_DIR}/data_rbac_250_19.html" ${SCENARIO_RBAC250}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_250_20.json" --write-html="${RESULT_DIR}/data_rbac_100_20.html" ${SCENARIO_RBAC250}

python3 ${POPULATE_SCRIPT} ${SCENARIO_RBAC300}

python3 ${TEST_SCRIPT} ${HOST} --request-per-second 1 --write="${RESULT_DIR}/data_rbac_300_01.json" --write-html="${RESULT_DIR}/data_rbac_300_01.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 2 --write="${RESULT_DIR}/data_rbac_300_02.json" --write-html="${RESULT_DIR}/data_rbac_300_02.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 3 --write="${RESULT_DIR}/data_rbac_300_03.json" --write-html="${RESULT_DIR}/data_rbac_300_03.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 4 --write="${RESULT_DIR}/data_rbac_300_04.json" --write-html="${RESULT_DIR}/data_rbac_300_04.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 5 --write="${RESULT_DIR}/data_rbac_300_05.json" --write-html="${RESULT_DIR}/data_rbac_300_05.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 6 --write="${RESULT_DIR}/data_rbac_300_06.json" --write-html="${RESULT_DIR}/data_rbac_300_06.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 7 --write="${RESULT_DIR}/data_rbac_300_07.json" --write-html="${RESULT_DIR}/data_rbac_300_07.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 8 --write="${RESULT_DIR}/data_rbac_300_08.json" --write-html="${RESULT_DIR}/data_rbac_300_08.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 9 --write="${RESULT_DIR}/data_rbac_300_09.json" --write-html="${RESULT_DIR}/data_rbac_300_09.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 10 --write="${RESULT_DIR}/data_rbac_300_10.json" --write-html="${RESULT_DIR}/data_rbac_300_10.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 11 --write="${RESULT_DIR}/data_rbac_300_11.json" --write-html="${RESULT_DIR}/data_rbac_300_11.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 12 --write="${RESULT_DIR}/data_rbac_300_12.json" --write-html="${RESULT_DIR}/data_rbac_300_12.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 13 --write="${RESULT_DIR}/data_rbac_300_13.json" --write-html="${RESULT_DIR}/data_rbac_300_13.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 14 --write="${RESULT_DIR}/data_rbac_300_14.json" --write-html="${RESULT_DIR}/data_rbac_300_14.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 15 --write="${RESULT_DIR}/data_rbac_300_15.json" --write-html="${RESULT_DIR}/data_rbac_300_15.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 16 --write="${RESULT_DIR}/data_rbac_300_16.json" --write-html="${RESULT_DIR}/data_rbac_300_16.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 17 --write="${RESULT_DIR}/data_rbac_300_17.json" --write-html="${RESULT_DIR}/data_rbac_300_17.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 18 --write="${RESULT_DIR}/data_rbac_300_18.json" --write-html="${RESULT_DIR}/data_rbac_300_18.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 19 --write="${RESULT_DIR}/data_rbac_300_19.json" --write-html="${RESULT_DIR}/data_rbac_300_19.html" ${SCENARIO_RBAC300}
python3 ${TEST_SCRIPT} ${HOST} --request-per-second 20 --write="${RESULT_DIR}/data_rbac_300_20.json" --write-html="${RESULT_DIR}/data_rbac_100_20.html" ${SCENARIO_RBAC300}

