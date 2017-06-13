#!/usr/bin/env bash

DIR=$1

cd ${DIR}

#JSON=data_1_1.json,data_1_5.json,data_1_10.json,data_1_15.json,data_1_20.json,data_1_25.json,data_2_1.json,data_2_5.json,data_2_10.json,data_2_15.json,data_2_20.json,data_2_25.json
#LEGEND="rbac 1 req/s,rbac 5 req/s,rbac 10 req/s,rbac 15 req/s,rbac 20 req/s,rbac 25 req/s,rbac+session 1 req/s,rbac+session 5 req/s,rbac+session 10 req/s,rbac+session 15 req/s,rbac+session 20 req/s,rbac+session 25 req/s"
#python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
#    --input="${JSON}" \
#    --legend="${LEGEND}" \
#    -d
JSON=data_1_1.json,data_1_5.json,data_1_10.json,data_2_1.json,data_2_5.json,data_2_10.json
LEGEND="rbac 1 req/s,rbac 5 req/s,rbac 10 req/s,rbac+session 1 req/s,rbac+session 5 req/s,rbac+session 10 req/s"
python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --input="${JSON}" \
    --legend="${LEGEND}" \
    -d


