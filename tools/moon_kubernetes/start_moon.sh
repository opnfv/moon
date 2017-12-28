#!/usr/bin/env bash

set -x

kubectl create namespace moon
kubectl create configmap moon-config --from-file tools/moon_kubernetes/conf/moon.conf -n moon
kubectl create configmap config --from-file ~/.kube/config -n moon
kubectl create configmap moon-policy-templates --from-file tests/functional/scenario_tests -n moon
kubectl create secret generic mysql-root-pass --from-file=tools/moon_kubernetes/conf/password_root.txt -n moon
kubectl create secret generic mysql-pass --from-file=tools/moon_kubernetes/conf/password_moon.txt -n moon

kubectl create -n moon -f tools/moon_kubernetes/templates/consul.yaml
kubectl create -n moon -f tools/moon_kubernetes/templates/db.yaml
kubectl create -n moon -f tools/moon_kubernetes/templates/keystone.yaml

echo =========================================
kubectl get pods -n moon
echo =========================================

sleep 10
kubectl create -n moon -f tools/moon_kubernetes/templates/moon_forming.yaml

echo Waiting for jobs forming
sleep 5
kubectl get jobs -n moon
kubectl logs -n moon jobs/forming

sleep 5
kubectl create -n moon -f tools/moon_kubernetes/templates/moon_manager.yaml

sleep 2
kubectl create -n moon -f tools/moon_kubernetes/templates/moon_orchestrator.yaml

kubectl create -n moon -f tools/moon_kubernetes/templates/moon_gui.yaml

# load moon_wrapper on both master and slaves
# moon_create_wrapper

