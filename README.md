# Moon
__Version 4.3__

This directory contains all the modules for running the Moon platform.

## Installation
### kubeadm
You must follow those explanations to install `kubeadm`:
> https://kubernetes.io/docs/setup/independent/install-kubeadm/

To summarize, you must install `docker`:
```bash
apt update
apt install -y docker.io
```
    
And then, install `kubeadm`:
```bash
apt update && apt install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
cat <<EOF >/etc/apt/sources.list.d/kubernetes.list
deb http://apt.kubernetes.io/ kubernetes-xenial main
EOF
apt update
apt install -y kubelet kubeadm kubectl
```

### Moon
The Moon code is not necessary to start the platform but you need
Kubernetes configuration files from the GIT repository. 

The easy way is to clone the Moon code:
```bash
git clone https://git.opnfv.org/moon
cd moon/moonv4
export MOON=$(pwd)
```

### OpenStack
You must have the following OpenStack components installed somewhere:
- nova, see [Nova install](https://docs.openstack.org/mitaka/install-guide-ubuntu/nova-controller-install.html)
- glance, see [Glance install](https://docs.openstack.org/glance/pike/install/)

A Keystone component is automatically installed and configured in the Moon platform.
After the Moon platform installation, the Keystone server will be available 
at: `http://localhost:30005 or http://\<servername\>:30005`

You can also use your own Keystone server if you want.

## Initialisation
### kubeadm
The `kubeadm` platform can be initialized with the following shell script:
```bash
sh kubernetes/init_k8s.sh
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

### Moon
The Moon platform is composed on the following components:
* `consul`: a Consul configuration server
* `db`: a MySQL database server
* `keystone`: a Keystone authentication server
* `gui`: a Moon web interface
* `manager`: the Moon manager for the database
* `orchestrator`: the Moon component that manage pods in te K8S platform
* `wrapper`: the Moon endpoint where OpenStack component connect to.

At this point, you must choose one of the following options:
* Specific configuration
* Generic configuration 

#### Specific Configuration
Why using a specific configuration:
1. The `db` and `keystone` can be installed by yourself but you must configure the 
Moon platform to use them.
2. You want to change the default passwords in the Moon platform

Use the following commands: `TODO`

#### Generic Configuration 
Why using a specific configuration:
1. You just want to test the platform
2. You want to develop on the Moon platform

The `Moon` platform can be initialized with the following shell script:
```bash
sh kubernetes/start_moon.sh
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

## Configuration
### Moon
#### Introduction
The Moon platform is already configured after the installation.
If you want to see or modify the configuration, go with a web browser 
to the following page: 

> http://localhost:30006

This is a consul server, you can update the configuration in the `KEY/VALUE` tab.
There are some configuration items, lots of them are only read when a new K8S pod is started
and not during its life cycle.

**WARNING: some confidential information are put here in clear text.
This is a known security issue.**

#### Keystone
If you have your own Keystone server, you can point Moon to your server in the 
`openstack/keystone` element or through the link: 
> http://localhost:30005/ui/#/dc1/kv/openstack/keystone/edit

This configuration element is read every time Moon need it, specially when adding users.

#### Database
The database can also be modified here: 
> http://varuna:30005/ui/#/dc1/kv/database/edit

**WARNING: the password is in clear text, this is a known security issue.**

If you want to use your own database server, change the configuration:

    {"url": "mysql+pymysql://my_user:my_secret_password@my_server/moon", "driver": "sql"}

Then you have to rebuild the database before using it. 
This can be done with the following commands:

    cd $MOON
    kubectl delete -f kubernetes/templates/moon_configuration.yaml
    kubectl create -f kubernetes/templates/moon_configuration.yaml


### OpenStack
Before updating the configuration of the OpenStack platform, check that the platform 
is working without Moon, use the following commands:
```bash    
# set authentication
openstack endpoint list
openstack user list
openstack server list
```

In order to connect the OpenStack platform with the Moon platform, you must update some
configuration files in Nova and Glance: 
* `/etc/nova/policy.json`
* `/etc/glance/policy.json`

In some installed platform, the `/etc/nova/policy.json` can be absent so you have 
to create one. You can find example files in those directory:
> ${MOON}/moonv4/templates/nova/policy.json
> ${MOON}/moonv4/templates/glance/policy.json

Each line is mapped to an OpenStack API interface, for example, the following line
allows the user to get details for every virtual machines in the cloud 
(the corresponding shell command is `openstack server list`):

    "os_compute_api:servers:detail": "",

This lines indicates that there is no special authorisation to use this API,
every users can use it. If you want that the Moon platform handles that authorisation, 
update this line with:

    "os_compute_api:servers:detail": "http://my_hostname:31001/authz"
    
1) by replacing `my_hostname` with the hostname (od the IP address) of the Moon platform.
2) by updating the TCP port (default: 31001) with the good one.

To find this TCP port, use the following command:

    $ kubectl get services -n moon | grep wrapper | cut -d ":" -f 2 | cut -d " " -f 1
    31002/TCP

### Moon
The Moon platform comes with a graphical user interface which can be used with 
a web browser at this URL:
> http://$MOON_HOST:30002

You will be asked to put a login and password. Those elements are the login and password 
of the Keystone server, if you didn't modify the Keystone server, you will find the 
login and password here:
> http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit 

**WARNING: the password is in clear text, this is a known security issue.**

The Moon platform can also be requested through its API:
> http://$MOON_HOST:30001

**WARNING: By default, no login/password will be needed because of 
the configuration which is in DEV mode.**

If you want more security, you have to update the configuration of the Keystone server here:
> http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit 

by modifying the `check_token` argument to `yes`.
If you write this modification, your requests to Moon API must always include a valid token 
taken from the Keystone server. This token must be place in the header of the request 
(`X-Auth-Token`).

## usage
### tests the platform
In order to know if the platform is healthy, here are some commands you can use.
1) Check that all the K8S pods in the Moon namespace are in running state:
`kubectl get pods -n moon`
    
2) Check if the Manager API is running:
```bash
curl http://$MOON_HOST:30001
curl http://$MOON_HOST:30001/pdp
curl http://$MOON_HOST:30001/policies
```
    
If you configured the authentication in the Moon platform:
```bash
curl -i \
  -H "Content-Type: application/json" \
  -d '
{ "auth": {
    "identity": {
      "methods": ["password"],
      "password": {
        "user": {
          "name": "admin",
          "domain": { "id": "default" },
          "password": "<set_your_password_here>"
        }
      }
    },
    "scope": {
      "project": {
        "name": "admin",
        "domain": { "id": "default" }
      }
    }
  }
}' \
  "http://moon_hostname:30006/v3/auth/tokens" ; echo
  
curl --header "X-Auth-Token: <token_retrieve_from_keystone>" http://moon_hostname:30001
curl --header "X-Auth-Token: <token_retrieve_from_keystone>" http://moon_hostname:30001/pdp
curl --header "X-Auth-Token: <token_retrieve_from_keystone>" http://moon_hostname:30001/policies
```
    
3) Use a web browser to navigate to the GUI and enter the login and password of the keystone service:
`firefox http://$MOON_HOST:30002`

4) Use tests Python Scripts
check firstly the Consul service for *Components/Manager*, e.g. 
```json
{
  "port": 8082, 
  "bind": "0.0.0.0", 
  "hostname": "manager", 
  "container": "wukongsun/moon_manager:v4.3.1", 
  "external": {
    "port": 30001, 
    "hostname": "$MOON_HOST"
  }
}
```
*OpenStack/Keystone*: e.g. 
```json
{
  "url": "http://keystone:5000/v3", 
  "user": "admin", 
  "password": "p4ssw0rd", 
  "domain": "default", 
  "project": "admin", 
  "check_token": false, 
  "certificate": false, 
  "external": {
    "url": "http://$MOON_HOST:30006/v3"
  }
}
```

```bash
python3 populate_default_values.py --consul-host=$MOON_HOST --consul-port=30005 -v scenario/rbac_large.py
python3 send_authz.py --consul-host=$MOON_HOST --consul-port=30005 --authz-host=$MOON_HOST --authz-port=31002 -v scenario/rbac_large.py
```
    
### GUI usage
After authentication, you will see 4 tabs: Project, Models, Policies, PDP:

* *Projects*: configure mapping between Keystone projects and PDP (Policy Decision Point)
* *Models*: configure templates of policies (for example RBAC or MLS)
* *Policies*: applied models or instantiated models ; 
on one policy, you map a authorisation model and set subject, objects and action that will
rely on that model
* *PDP*: Policy Decision Point, this is the link between Policies and Keystone Project

In the following paragraphs, we will add a new user in OpenStack and allow her to list 
all VM on the OpenStack platform.

First, add a new user and a new project in the OpenStack platform:

      openstack user create --password-prompt demo_user
      openstack project create demo
      DEMO_USER=$(openstack user list | grep demo_user | cut -d " " -f 2)
      DEMO_PROJECT=$(openstack project list | grep demo | cut -d " " -f 2)
      openstack role add --user $DEMO_USER --project $DEMO_PROJECT admin
      
You have to add the same user in the Moon interface:

1. go to the `Projects` tab in the Moon interface
1. go to the line corresponding to the new project and click to the `Map to a PDP` link
1. select in the combobox the MLS PDP and click `OK`
1. in the Moon interface, go to the `Policy` tab
1. go to the line corresponding to the MLS policy and click on the `actions->edit` button
1. scroll to the `Perimeters` line and click on the `show` link to show the perimeter configuration
1. go to the `Add a subject` line and click on `Add a new perimeter`
1. set the name of that subject to `demo_user` (*the name must be strictly identical*)
1. in the combobox named `Policy list` select the `MLS` policy and click on the `+` button
1. click on the yellow `Add Perimeter` button
1. go to the `Assignment` line and click on the `show` button
1. under the `Add a Assignments Subject` select the MLS policy, 
the new user (`demo_user`), the category `subject_category_level` 
1. in the `Select a Data` line, choose the `High` scope and click on the `+` link 
1. click on the yellow `Create Assignments` button 
1. if you go to the OpenStack platform, the `demo_user` is now allow to connect 
to the Nova component (test with `openstack server list` connected with the `demo_user`)


## Annexes

### connect to the OpenStack platform

Here is a shell script to authenticate to the OpenStack platform as `admin`:

    export OS_USERNAME=admin
    export OS_PASSWORD=p4ssw0rd
    export OS_REGION_NAME=Orange
    export OS_TENANT_NAME=admin
    export OS_AUTH_URL=http://moon_hostname:30006/v3
    export OS_DOMAIN_NAME=Default
    export OS_IDENTITY_API_VERSION=3

For the `demo_user`, use:

    export OS_USERNAME=demo_user
    export OS_PASSWORD=your_secret_password
    export OS_REGION_NAME=Orange
    export OS_TENANT_NAME=demo
    export OS_AUTH_URL=http://moon_hostname:30006/v3
    export OS_DOMAIN_NAME=Default
    export OS_IDENTITY_API_VERSION=3

