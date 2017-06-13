#!/usr/bin/env bash

DIR=$1

cd ${DIR}

python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --input="data_1.json,data_2.json,data_3.json,data_4.json,data_5.json,data_10.json,data_15.json,data_20.json" \
    --legend="1 req/s,2 req/s,3 req/s,4 req/s,5 req/s,10 req/s,15 req/s,20 req/s" \
    --plot-result="Deny" \
    --plot-average \
    -d
#python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
#    --input="data_1.json,data_5.json,data_10.json,data_15.json,data_20.json" \
#    --legend="1 req/s,5 req/s,10 req/s,15 req/s,20 req/s" \
#    -d
#python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
#    --input="data_1.json,data_2.json,data_3.json,data_4.json,data_5.json,data_10.json,data_15.json,data_20.json,data_25.json" \
#    --legend="1 req/s,2 req/s,3 req/s,4 req/s,5 req/s,10 req/s,15 req/s,20 req/s,25 req/s" \
#    -d
