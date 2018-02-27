# Moon
__Version 4.3__
This directory contains all the modules for running the Moon platform.


## Platform 
### Setup
- [Docker installation](tools/moon_kubernetes/README.md)
- [kubeadm installation](tools/moon_kubernetes/README.md)
- [Moon deployment](tools/moon_kubernetes/README.md)
- [OpenStack deployment](tools/openstack/README.md)

### Micro-service Architecture
The Moon platform is composed on the following components/containers:
- *consul*: a Consul configuration server
- *db*: a MySQL database server
- *keystone*: a Keystone authentication server
- [gui](moon_gui/README.md): a Moon web interface
- [manager](moon_manager/README.md): the Moon manager for the database
- [orchestrator](moon_orchestrator/README.md): the Moon component that manage pods in te K8S platform
- [wrapper](moon_wrapper/README.md): the Moon endpoint where OpenStack component connect to.


## Manipulation
### moon_gui
The web access of Moon is through the URL `http://$MOON_HOST:30002` with the login and password of Keystone.
The default login and password can be found here: `http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit`.  

**WARNING: the password is in clear text, this is a known security issue.**

### moon_manager
The REST access of Moon is through `http://$MOON_HOST:30001`

**WARNING: By default, no login/password will be needed because of the configuration which is in DEV mode.**

For more security, update `http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit` by modifying the `check_token` argument to `yes`
Requests to Moon API must include a valid token taken from Keystone in the header of `X-Auth-Token`.

Check if the Manager API is running with:
```bash
curl http://$MOON_HOST:30001
curl http://$MOON_HOST:30001/pdp
curl http://$MOON_HOST:30001/policies
```

The Moon platform is fully installed and configured when you have no error with the `moon_get_keystone_projects`:
```bash
sudo pip install python_moonclient --upgrade
moon project list
```

### moon_wrapper
The moon_wrapper component is used to connect OpenStack to the Moon platform.
You need to load one wrapper before connecting OpenStack to Moon.
First of all, get the names of all available slaves:
```bash
moon slave list
```
Select the slave you want to configure:
```bash
moon slave set <name_of_the_slave>
```
If you don't put a name here, by default, the script will use `kubernetes-admin@kubernetes`
which is the master.

If you need to unload the slave, use the following command:
```bash
moon slave delete <name_of_the_slave>
```
If you don't put a name here, by default, the script will use `kubernetes-admin@kubernetes`.

### inport/export of the moon database
Using the moon python client, it is possible to export and import the content of the moon database. The format of the file must be json. Examples of files that can be imported are found in the moon_manager package (rbac.json and mls.json)

The relations between different elements of the json in made using their names. Therefore, the name acts, for now, as a unique identifier in the json files. Importing several times the same json file can lead to unexpected behavior. It is advised to import json file in an empty database.

Two particular entries in the json description are used to specify the way of performing the import:
 - "mandatory": it can be true or false. This field is only valid for policies description. The policy having this field set to true, will be automatically added to the other elements of the json file that have an empty "policy" field (subject data for instance) or that have a "policies" field which does not already contain the mandatory policy name (such as subjects). 
 - "override" : it can be true or false. This field is only valid for policies and models. If set to true and a policy/model with an identical name already exists in the database, it will be overwritten.


## Tests
- [Python Unit Test](tests/python_unit/README.md)
- [Functional Test](tests/functional/README.md)


## Annexe
### Authentication
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
