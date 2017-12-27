#!/usr/bin/env bash

set -x

kubectl create namespace moon
kubectl create configmap moon-config --from-file conf/moon.conf -n moon
kubectl create configmap config --from-file ~/.kube/config -n moon
kubectl create configmap moon-policy-templates --from-file ../../tests/functional/scenario_enabled -n moon
kubectl create secret generic mysql-root-pass --from-file=conf/password_root.txt -n moon
kubectl create secret generic mysql-pass --from-file=conf/password_moon.txt -n moon

kubectl create -n moon -f templates/consul.yaml
kubectl create -n moon -f templates/db.yaml
kubectl create -n moon -f templates/keystone.yaml

echo =========================================
kubectl get pods -n moon
echo =========================================

sleep 10
kubectl create -n moon -f templates/moon_forming.yaml

echo Waiting for jobs forming
sleep 5
kubectl get jobs -n moon
kubectl logs -n moon jobs/forming

sleep 5
kubectl create -n moon -f templates/moon_manager.yaml

sleep 2
kubectl create -n moon -f templates/moon_orchestrator.yaml

kubectl create -n moon -f templates/moon_gui.yaml


