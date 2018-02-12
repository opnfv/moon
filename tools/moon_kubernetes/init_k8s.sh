#!/usr/bin/env bash

set -x

sudo kubeadm reset

sudo swapoff -a

sudo kubeadm init --pod-network-cidr=192.168.0.0/16 # network for Calico
#sudo kubeadm init --pod-network-cidr=10.244.0.0/16 # network for Canal

mkdir -p $HOME/.kube
sudo cp -f /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

kubectl apply -f http://docs.projectcalico.org/v2.4/getting-started/kubernetes/installation/hosted/kubeadm/1.6/calico.yaml
#kubectl apply -f https://raw.githubusercontent.com/projectcalico/canal/master/k8s-install/1.6/rbac.yaml
#kubectl apply -f https://raw.githubusercontent.com/projectcalico/canal/master/k8s-install/1.6/canal.yaml

#kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml

#kubectl delete deployment kube-dns --namespace=kube-system
#kubectl apply -f tools/moon_kubernetes/templates/kube-dns.yaml

kubectl taint nodes --all node-role.kubernetes.io/master- # make the master also as a node

kubectl proxy&
sleep 5
echo =========================================
kubectl get po --namespace=kube-system
echo =========================================


