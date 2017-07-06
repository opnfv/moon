#!/usr/bin/env bash

DIR=$1

# cd ${DIR}

#JSON=data_1_1.json,data_1_5.json,data_1_10.json,data_1_15.json,data_1_20.json,data_1_25.json,data_2_1.json,data_2_5.json,data_2_10.json,data_2_15.json,data_2_20.json,data_2_25.json
#LEGEND="rbac 1 req/s,rbac 5 req/s,rbac 10 req/s,rbac 15 req/s,rbac 20 req/s,rbac 25 req/s,rbac+session 1 req/s,rbac+session 5 req/s,rbac+session 10 req/s,rbac+session 15 req/s,rbac+session 20 req/s,rbac+session 25 req/s"
#python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
#    --input="${JSON}" \
#    --legend="${LEGEND}" \
#    -d

cd results/01

JSON=data_rbac_1_01.json,data_rbac_2_01.json,data_rbac_3_01.json,data_rbac_4_01.json,data_rbac_5_01.json
LEGEND="10 users,20 users,30 users,40 users,50 users"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --legend="${LEGEND}" \
    --plot-result="*" \
    --write-html="rbac_10-50users_1reqs.html" \
    digraph \
    average \
    "${JSON}"

sleep 1

JSON=data_rbac_1_10.json,data_rbac_2_10.json,data_rbac_3_10.json,data_rbac_4_10.json,data_rbac_5_10.json
LEGEND="10 users,20 users,30 users,40 users,50 users"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --legend="${LEGEND}" \
    --plot-result="*" \
    --write-html="rbac_10-50users_10reqs.html" \
    digraph \
    average \
    "${JSON}"

sleep 1

JSON=data_rbac_1_20.json,data_rbac_2_20.json,data_rbac_3_20.json,data_rbac_4_20.json,data_rbac_5_20.json
LEGEND="10 users,20 users,30 users,40 users,50 users"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --legend="${LEGEND}" \
    --plot-result="*" \
    --write-html="rbac_20-50users_20reqs.html" \
    digraph \
    average \
    "${JSON}"

sleep 1

JSON=data_rbac_1_30.json,data_rbac_2_30.json,data_rbac_3_30.json,data_rbac_4_30.json,data_rbac_5_30.json
LEGEND="10 users,20 users,30 users,40 users,50 users"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --legend="${LEGEND}" \
    --plot-result="*" \
    --write-html="rbac_30-50users_30reqs.html" \
    digraph \
    average \
    "${JSON}"

sleep 1

JSON=data_rbac_1_39.json,data_rbac_2_39.json,data_rbac_3_39.json,data_rbac_4_39.json,data_rbac_5_39.json
LEGEND="10 users,20 users,30 users,40 users,50 users"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --legend="${LEGEND}" \
    --plot-result="*" \
    --write-html="rbac_39-50users_39reqs.html" \
    digraph \
    average \
    "${JSON}"

sleep 1

