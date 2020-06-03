#!/usr/bin/env bash

set +x

kubectl delete -n moon -f tools/moon_kubernetes/templates/moon_orchestrator.yaml
for i in $(kubectl get deployments -n moon | grep wrapper | cut -d  " " -f 1 | xargs); do
    echo deleting $i
    kubectl delete deployments/$i -n moon;
done
for i in $(kubectl get deployments -n moon | grep pipeline | cut -d  " " -f 1 | xargs); do
    echo deleting $i
    kubectl delete deployments/$i -n moon;
done
for i in $(kubectl get services -n moon | grep wrapper | cut -d  " " -f 1 | xargs); do
    echo deleting $i
    kubectl delete services/$i -n moon;
done
for i in $(kubectl get services -n moon | grep pipeline | cut -d  " " -f 1 | xargs); do
    echo deleting $i
    kubectl delete services/$i -n moon;
done

if [ "$1" = "build" ]; then

    DOCKER_ARGS=""

    cd moon_manager
    docker build -t wukongsun/moon_manager:v4.3.1 . ${DOCKER_ARGS}
    if [ "$2" = "push" ]; then
        docker push wukongsun/moon_manager:v4.3.1
    fi
    cd -

    cd moon_orchestrator
    docker build -t wukongsun/moon_orchestrator:v4.3 . ${DOCKER_ARGS}
    if [ "$2" = "push" ]; then
        docker push wukongsun/moon_orchestrator:v4.3
    fi
    cd -

    cd moon_interface
    docker build -t wukongsun/moon_interface:v4.3 . ${DOCKER_ARGS}
    if [ "$2" = "push" ]; then
        docker push wukongsun/moon_interface:v4.3
    fi
    cd -

    cd moon_authz
    docker build -t wukongsun/moon_authz:v4.3 . ${DOCKER_ARGS}
    if [ "$2" = "push" ]; then
        docker push wukongsun/moon_authz:v4.3
    fi
    cd -

    cd moon_wrapper
    docker build -t wukongsun/moon_wrapper:v4.3 . ${DOCKER_ARGS}
    if [ "$2" = "push" ]; then
        docker push wukongsun/moon_wrapper:v4.3
    fi
    cd -
fi
