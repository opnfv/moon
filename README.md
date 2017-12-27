# Moon
__Version 4.3__

This directory contains all the modules for running the Moon platform.

## Platform Setup
- [Docker installation](tools/moon_kubernetes/README.md)
- [kubeadm installation](tools/moon_kubernetes/README.md)
- [Moon deployment](tools/moon_kubernetes/README.md)
- [OpenStack deployment](tools/openstack/README.md)


## Micro-service Architecture
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
The Moon platform comes with a graphical user interface which can be used with 
a web browser at this URL `http://$MOON_HOST:30002`

You will be asked to put a login and password. Those elements are the login and password 
of the Keystone server, if you didn't modify the Keystone server, you will find the 
login and password here `http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit` 

**WARNING: the password is in clear text, this is a known security issue.**

### moon_manager
The Moon platform can also be requested through its API `http://$MOON_HOST:30001`

**WARNING: By default, no login/password will be needed because of 
the configuration which is in DEV mode.**

If you want more security, you have to update the configuration of the Keystone server here:
`http://$MOON_HOST:30005/ui/#/dc1/kv/openstack/keystone/edit` 
by modifying the `check_token` argument to `yes`.
If you write this modification, your requests to Moon API must always include a valid token 
taken from the Keystone server. This token must be place in the header of the request 
(`X-Auth-Token`).

### End-to-end Functional Test
Check if the Manager API is running:
```bash
curl http://$MOON_HOST:30001
curl http://$MOON_HOST:30001/pdp
curl http://$MOON_HOST:30001/policies
```

### Consul Check
Check the Consul service for 
- *Components/Manager*, e.g. 
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
- *OpenStack/Keystone*: e.g. 
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

### Tests
Launch functional [test scenario](tests/functional/scenario_enabled) : 
```bash
sudo pip install python_moonclient --upgrade
cd $MOON_HOME/tests/functional/scenario_tests
moon_populate_values --consul-host=$MOON_HOST --consul-port=30005 -v rbac_large.py
moon_send_authz --consul-host=$MOON_HOST --consul-port=30005 --authz-host=$AUTHZ_HOST --authz-port=$AUTHZ_PORT -v rbac_large.py
```

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