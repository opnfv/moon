# Moon Platform Setup
## Docker Installation
```bash
apt update
apt install -y docker.io
```

## K8S Installation
Choose the right K8S platform
### Minikube
```bash
curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/kubectl
curl -Lo minikube https://storage.googleapis.com/minikube/releases/v0.21.0/minikube-linux-amd64 && chmod +x minikube && sudo mv minikube /usr/local/bin/
```

### Kubeadm
see: https://kubernetes.io/docs/setup/independent/install-kubeadm/
```bash
apt-get update && apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt-get update
apt-get install -y kubelet kubeadm kubectl
```

## Moon Deployment
### Initiate K8S
```bash
cd $MOON_HOME
bash tools/moon_kubernes/init_k8s.sh
```

Wait until all the kubeadm containers are in the `running` state:
```bash
watch kubectl get po --namespace=kube-system
```
    
You must see something like this:

    $ kubectl get po --namespace=kube-system
    NAME                                        READY     STATUS    RESTARTS   AGE
    calico-etcd-7qgjb                           1/1       Running   0          1h
    calico-node-f8zvm                           2/2       Running   1          1h
    calico-policy-controller-59fc4f7888-ns9kv   1/1       Running   0          1h
    etcd-varuna                                 1/1       Running   0          1h
    kube-apiserver-varuna                       1/1       Running   0          1h
    kube-controller-manager-varuna              1/1       Running   0          1h
    kube-dns-bfbb49cd7-rgqxn                    3/3       Running   0          1h
    kube-proxy-x88wg                            1/1       Running   0          1h
    kube-scheduler-varuna                       1/1       Running   0          1h


### Deploy Moon
```bash
cd $MOON_HOME
sudo bash tools/moon_kubernes/start_moon.sh
```

Wait until all the Moon containers are in the `running` state:
```bash
watch kubectl get po --namespace=moon
```

You must see something like this:

    $ kubectl get po --namespace=moon
    NAME                                   READY     STATUS    RESTARTS   AGE
    consul-57b6d66975-9qnfx                1/1       Running   0          52m
    db-867f9c6666-bq8cf                    1/1       Running   0          52m
    gui-bc9878b58-q288x                    1/1       Running   0          51m
    keystone-7d9cdbb69f-bl6ln              1/1       Running   0          52m
    manager-5bfbb96988-2nvhd               1/1       Running   0          51m
    manager-5bfbb96988-fg8vj               1/1       Running   0          51m
    manager-5bfbb96988-w9wnk               1/1       Running   0          51m
    orchestrator-65d8fb4574-tnfx2          1/1       Running   0          51m
    wrapper-astonishing-748b7dcc4f-ngsvp   1/1       Running   0          51m
    
### Docker-K8S Port Mapping
```yamlex
manager:
    port: 8082
    kport: 30001
gui:
    port: 3000
    kport: 30002
orchestrator:
    port: 8083
    kport: 30003
consul:
    port: 8500
    kport: 30005
keystone:
    port: 5000
    kport: 30006
wrapper:
    port: 8080
    kport: 30010
interface:
    port: 8080
authz:
    port: 8081
```
