#!/bin/bash
#number of pods type that should be running or be stopped
declare -i pods_to_check=0
 #global variable on current namespace to check
current_namespace=""
#if set to 1 we check that the pods are running, otherwise we chack that the pods are stopped
declare -i check_running=1
#name of the pod to check
match_pattern=""
#postfix used to recognize pods name
OS="unknown_os"

#this function checks if a pod with name starting with $1 is in the Running / Stopped state depending on $heck_running
#   $1 : the name the pods starts with (without the random string added by kubernate to the pod name)
#   $2 : either the number of identical pods that shall be run or #
#   $3 : if $2 is #, the number of lines of the pods name appear on which the pod appears
function check_pod() {
   declare -i nb_arguments=$#
   match_pattern="$1"; shift
   if [ $nb_arguments -gt 2 ]; then
         shift; declare -i nb_pods_pattern="$1"
         if [ $check_running -eq 1 ]; then #check if pods are running
             declare -i result=$(sudo kubectl get po --namespace=${current_namespace} | grep  $match_pattern | grep "1/1" | grep -c "Running")
             if [ $result -eq $nb_pods_pattern ]; then
                pods_to_check=$pods_to_check+1
             fi
         else #check if pods are stopped
             declare -i result=$(sudo kubectl get po --namespace=${current_namespace} | grep  $match_pattern | grep -c "Running\|Terminating")
             if [ $result -eq 0 ]; then
                pods_to_check=$pods_to_check+1
             fi
         fi
   else
         declare -i nb=$1
         if [ $check_running -eq 1 ]; then #check if pods are running
             declare -i result=$(sudo kubectl get po --namespace=${current_namespace} |  grep  $match_pattern | grep "$nb/$nb" | grep -c "Running")
             if [ $result -eq 1 ]; then
                pods_to_check=$pods_to_check+1
             fi
         else #check if pods are stopped
             declare -i result=$(sudo kubectl get po --namespace=${current_namespace} |  grep  $match_pattern | grep -c "Running\|Terminating")
             if [ $result -eq 0 ]; then
                pods_to_check=$pods_to_check+1
             fi
         fi
   fi
}

#this function tests a list of pods
function check_pods() {
    current_namespace="${1}"; shift
    pods=("${@}")
    declare -i pods_nb=${#pods[@]}
    sleep 2
    while [ $pods_to_check -lt $pods_nb ]
    do
        pods_to_check=0
        for node in "${pods[@]}"
        do
            check_pod $node
        done

        if [ $check_running -eq 1 ]; then
            echo -ne "$pods_to_check node types on $pods_nb are running...\033[0K\r"
        else
            declare -i running_pods=$pods_nb-$pods_to_check
            echo -ne "$running_pods node types on $pods_nb are still running...\033[0K\r"
        fi
        sleep 2
    done
}

#this function checks if a list of pods ($2) in a specific namspace ($1) are in the Running state
function check_pods_running() {
   check_running=1
   check_pods "${@}"
   pods_to_check=0
}

#this function checks if a list of pods ($2) are not in a specific namspace ($1)
function check_pods_not_running() {
   check_running=0
   check_pods "${@}"
   pods_to_check=0
}

function wait_for_kubernate_calico() {
  echo -ne "Waiting for kubernate... "
  kube_namespace="kube-system"
  declare -a kube_pods=("calico-etcd 1" "calico-node 2" "calico-policy-controller 1" "etcd-${OS} 1" "kube-apiserver-${OS} 1" "kube-controller-manager-${OS} 1" "kube-dns 3" "kube-proxy 1" "kube-scheduler-${OS} 1")
  check_pods_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_init() {
 echo "Waiting for moon (consul, db, keystone) ..."
 kube_namespace="moon"
 declare -a kube_pods=("consul 1" "db 1" "keystone 1")
 check_pods_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_forming() {
 echo "Waiting for moon (forming) ..."
 kube_namespace="moon"
 declare -a kube_pods=("forming 1")
 check_pods_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_manager() {
 echo "Waiting for moon (manager) ..."
 kube_namespace="moon"
 declare -a kube_pods=("manager # 1")
 check_pods_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_end() {
 echo "Waiting for moon (orchestrator, gui) ..."
 kube_namespace="moon"
 declare -a kube_pods=("gui 1" "orchestrator 1")
 check_pods_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_forming_to_end() {
 echo "Waiting for moon forming to finish initialization. This can take few minutes..."
 kube_namespace="moon"
 declare -a kube_pods=("forming 1")
 check_pods_not_running "$kube_namespace" "${kube_pods[@]}"
}

function wait_for_moon_delete_to_end(){
  echo "Waiting for moon to terminate..."
  kube_namespace="moon"
  declare -a kube_pods=("consul 1" "db 1" "keystone 1" "manager # 3" "gui 1" "orchestrator 1")
  check_pods_not_running "$kube_namespace" "${kube_pods[@]}"
}

function check_os(){
 if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=${ID}
 elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
    declare -i result=$(grep -i "debian" $OS)
    if [ $result -eq 1 ]; then
        OS="debian"
    fi
    declare -i result=$(grep -i "ubuntu" $OS)
    if [ $result -eq 1 ]; then
        OS="ubuntu"
    fi
 elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
    declare -i result=$(grep -i "debian" $OS)
    if [ $result -eq 1 ]; then
        OS="debian"
    fi
    declare -i result=$(grep -i "ubuntu" $OS)
    if [ $result -eq 1 ]; then
        OS="ubuntu"
    fi
 elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    declare -i result=$(grep -i "debian" $OS)
    if [ $result -eq 1 ]; then
        OS="debian"
    fi
    declare -i result=$(grep -i "ubuntu" $OS)
    if [ $result -eq 1 ]; then
        OS="ubuntu"
    fi
 elif [ -f /etc/SuSe-release ]; then
    # Older SuSE/etc.
    echo "TO DO : get the name of the OS at the end of the pods name"
 elif [ -f /etc/redhat-release ]; then
    # Older Red Hat, CentOS, etc.
    echo "TO DO : get the name of the OS at the end of the pods name"
 else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
    echo "TO DO : get the name of the OS at the end of the pods name"
 fi
 echo "postfix used to detect pods name : ${OS}"
}

declare -i nb_arguments=$#
declare -i init_kubernate=1

if [ $# -eq 1 ]; then
    if [ $1 == "moon" ]; then
       init_kubernate=0
    fi

    if [ $1 == "-h" ]; then
       echo "Usage : "
       echo " - 'bash tools/moon_kubernetes/init_k8s_moon.sh'        launches the kubernates platform and the moon platform."
       echo " - 'bash tools/moon_kubernetes/init_k8s_moon.sh moon'   launches the moon platform only. If the moon platform is already launched, it deletes and recreates it."
       echo " "
    fi
fi

if [ $init_kubernate -eq 1 ]; then
    check_os
    echo "=============================="
    echo "Launching kubernate  "
    echo "=============================="
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

    kubectl delete deployment kube-dns --namespace=kube-system
    kubectl apply -f tools/moon_kubernetes/templates/kube-dns.yaml
    kubectl taint nodes --all node-role.kubernetes.io/master- # malke the master also as a node

    kubectl proxy&

    wait_for_kubernate_calico

    echo "=============================="
    echo "Kubernate platform is ready ! "
    echo "=============================="
fi

echo "============================"
echo "Launching moon "
echo "============================"
#check if the moon platform is running, if so we terminate it
declare -i moon_is_running=$(sudo kubectl get namespace | grep -c moon)
if [ $moon_is_running -eq 1 ]; then
    sudo kubectl delete namespace moon
    wait_for_moon_delete_to_end
    sleep 2
fi

#launching moon
kubectl create namespace moon
kubectl create configmap moon-config --from-file tools/moon_kubernetes/conf/moon.conf -n moon
kubectl create configmap config --from-file ~/.kube/config -n moon
kubectl create configmap moon-policy-templates --from-file tests/functional/scenario_tests -n moon
kubectl create secret generic mysql-root-pass --from-file=tools/moon_kubernetes/conf/password_root.txt -n moon
kubectl create secret generic mysql-pass --from-file=tools/moon_kubernetes/conf/password_moon.txt -n moon

kubectl create -n moon -f tools/moon_kubernetes/templates/consul.yaml
kubectl create -n moon -f tools/moon_kubernetes/templates/db.yaml
kubectl create -n moon -f tools/moon_kubernetes/templates/keystone.yaml
wait_for_moon_init


kubectl create -n moon -f tools/moon_kubernetes/templates/moon_forming.yaml
wait_for_moon_forming


kubectl create -n moon -f tools/moon_kubernetes/templates/moon_manager.yaml
wait_for_moon_manager


kubectl create -n moon -f tools/moon_kubernetes/templates/moon_orchestrator.yaml
kubectl create -n moon -f tools/moon_kubernetes/templates/moon_gui.yaml
wait_for_moon_end

#wait the end of pods initialization performed by moon forming
wait_for_moon_forming_to_end

echo "==========================                   "
echo "Moon platform is ready !"
echo "=========================="


