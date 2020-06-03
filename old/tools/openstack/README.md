# OpenStack
## Installation
For the *Moon* platform, you must have the following OpenStack components installed somewhere:
- *Nova*, see [Nova install](https://docs.openstack.org/mitaka/install-guide-ubuntu/nova-controller-install.html)
- *Glance*, see [Glance install](https://docs.openstack.org/glance/pike/install/)
- *Keystone* is automatically installed and configured in the Moon platform.
After the Moon platform installation, the Keystone server will be available 
at: `http://localhost:30005 or http://\<servername\>:30005`

You can also use your own Keystone server if you want.

## Configuration
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
- `/etc/nova/policy.json`
- `/etc/glance/policy.json`

In some installed platform, the `/etc/nova/policy.json` can be absent so you have 
to create one. You can find example files in those directory:
- `${MOON}/tools/openstack/nova/policy.json`
- `${MOON}/tools/openstack/glance/policy.json`

Each line is mapped to an OpenStack API interface, for example, the following line
allows the user to get details for every virtual machines in the cloud 
(the corresponding shell command is `openstack server list`):

    "os_compute_api:servers:detail": "",

This lines indicates that there is no special authorisation to use this API,
every users can use it. If you want that the Moon platform handles that authorisation, 
update this line with:

    "os_compute_api:servers:detail": "http://my_hostname:31001/authz"
    
1) by replacing `my_hostname` with the hostname (or the IP address) of the Moon platform.
2) by updating the TCP port (default: 31001) with the good one.

To find this TCP port, use the following command:

    $ kubectl get services -n moon | grep wrapper | cut -d ":" -f 2 | cut -d " " -f 1
    31002/TCP

## Tests
Here is a shell script to authenticate to the OpenStack platform as `admin`:
```bash
export OS_USERNAME=admin
export OS_PASSWORD=p4ssw0rd
export OS_REGION_NAME=Orange
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://moon_hostname:30006/v3
export OS_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3
```
  
For the `demo_user`, use:
```bash
export OS_USERNAME=demo_user
export OS_PASSWORD=your_secret_password
export OS_REGION_NAME=Orange
export OS_TENANT_NAME=demo
export OS_AUTH_URL=http://moon_hostname:30006/v3
export OS_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3
```
