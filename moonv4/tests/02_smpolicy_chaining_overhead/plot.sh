#!/usr/bin/env bash

DIR=$1

cd ${DIR}

python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py --help

python3 ${MOON_HOME}/moon_interface/tests/apitests/plot_json.py \
    --input="data_1.json,data_2.json,data_3.json,data_4.json,data_5.json,data_6.json,data_7.json,data_8.json,data_9.json,data_10.json,data_11.json,data_12.json,data_13.json,data_14.json,data_15.json,data_16.json,data_17.json,data_18.json,data_19.json,data_20.json,data_21.json,data_22.json,data_23.json,data_24.json,data_25.json,data_26.json,data_27.json,data_28.json,data_29.json,data_30.json" \
    --legend="1 req/s,2 req/s,3 req/s,4 req/s,5 req/s,6 req/s,7 req/s,8 req/s,9 req/s,10 req/s,11 req/s,12 req/s,13 req/s,14 req/s,15 req/s,16 req/s,17 req/s,18 req/s,19 req/s,20 req/s,21 req/s,22 req/s,23 req/s,24 req/s,25 req/s,26 req/s,27 req/s,28 req/s,29 req/s,30 req/s" \
    --plot-result="*" \
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
