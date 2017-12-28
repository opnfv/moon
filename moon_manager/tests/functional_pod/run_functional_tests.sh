#!/usr/bin/env bash

set -x

kubectl create -n moon -f tools/moon_kubernetes/templates/moon_forming.yaml

echo Waiting for jobs forming
sleep 5
kubectl get jobs -n moon
kubectl logs -n moon jobs/forming

