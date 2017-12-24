# Moon Platform Setup
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
### Creation
Execute the script : init_k8s.sh
```bash
sudo bash init_k8s.sh
watch kubectl get po --namespace=kube-system
```
Wait until all pods are in "Running" state (crtl-c to stop the watch command)

### Execution
Execute the script : start_moon.sh
```bash
sudo bash start_moon.sh
watch kubectl get po --namespace=moon
```

