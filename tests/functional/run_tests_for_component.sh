#!/usr/bin/env bash

CUR_PWD=$(pwd)
INPUT_FILE=../tools/moon_kubernetes/templates/moon_forming_functest.yaml
OUTPUT_FILE=tests/functional_pod/moon_forming_functest.yaml

echo current working directory: ${CUR_PWD}

cat ${INPUT_FILE} | sed "s|{{PATH}}|${CUR_PWD}|" > ${OUTPUT_FILE}

kubectl create -f moon_forming_functest.yaml

sleep 5

echo "waiting for FuncTests (it may takes time)..."
echo -e "\033[35m"
sed '/<END OF JOB>/q' <(kubectl logs -n moon jobs/functest -f)
echo -e "\033[m"

kubectl delete -f moon_forming_functest.yaml
