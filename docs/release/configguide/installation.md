# Build Python Packages and Docker Images

## Python Package
### pre-requist
Get the code
```bash
git clone https://git.opnfv.org/moon
cd moon/moonv4
export MOON_HOME=$(pwd)
sudo ln -s $(pwd)/conf /etc/moon
```

Install python wheel
```bash
sudo apt install python3-wheel
```

Install pip twine
```bash
sudo pip install twine
```

Package code, wheel is a new format instead of `tar.gz`
```bash
python setup.py sdist bdist_wheel
```

Upload to PyPi
```bash
twine upload dist/moon_xxx-y.y.y.whl
twine upload dist/moon_xxx-y.y.y.tar.gz
```

Install a package from PyPi
```bash
sudo pypi install moon_xxx --upgrade
```

### moon_db
- change version in `moon_db/__init__.py`
- add `Changelog`

### moon_utilities
- change version in `moon_utilities/__init__.py`
- add `Changelog`

### moon_orchestrator
- change version in `moon_orchestrator/__init__.py`
- add `Changelog`


### Build All Pip
```bash
sudo pip3 install pip --upgrade
cd ${MOON_HOME}/bin
source build_all_pip.sh
```


## Container
## keystone_mitaka
see `templates/docker/keystone/README.md` to build the `keystone_mitaka` container


### moon_router

 
### moon_interface


### moon_manager


### moon_authz


### moon_gui


## How to hack the Moon platform
### Force the build of components

If you want to rebuild one or more component, you have to modify the configuration file `moon.conf`. 

For example, if you want to rebuild the moon_interface, got to the `[interface]` section and delete the 
value of the container key like this:

```
[interface]
host=172.18.0.11
port=38001
# Name of the container to download (if empty build from scratch)
# example: container=moon/moon_interface:latest
container=
```

You can configure the interface, the router and both the security_function and security_policy.
You can also force the version of the component like this: `container=moon/moon_interface:4.0.0`

### Update the moon_interface

Go to the directory `${MOON_HOME}/moon_interface` and update the code accordingly to your needs,
then update the python package.

```bash
cd ${MOON_HOME}/moon_interface
python setup.py sdist
cp dist/moon_interface_* ../moon_orchestrator/dist
# kill moon_orchestrator if needed and restart it
```

### Update the moon_secrouter

Go to the directory `${MOON_HOME}/moon_secrouter` and update the code accordingly to your needs,
then update the python package.

```bash
cd ${MOON_HOME}/moon_secrouter
python setup.py sdist
cp dist/moon_secrouter* ../moon_orchestrator/dist
# kill moon_orchestrator if needed and restart it
```

## Problems that may arise

If the moon_orchestrator doesn't want to start
(with, for example, the following error: `docker.errors.APIError: 409 Client Error: Conflict`),
check if the router and interface containers still exist and kill and delete them:

```bash
docker kill moon_interface
docker kill moon_router
docker rm moon_interface
docker rm moon_router
```

If the moon_orchestrator complains that it cannot request the RabbitMQ server,
check if the messenger server is up and running:

```bash
docker ps
# you must see the messenger running here
# if not, restart it
docker run -dti --net=moon --hostname messenger --name messenger --link messenger:messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -p 5671:5671 -p 5672:5672 rabbitmq:3-management
```

## Configure DB
### Relaunch Keystone docker
If error of `get_keystone_projects()`, then relaunch the Keystone docker, and wait 40 seconds!!!
```bash
docker rm -f keystone
docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka
```

### Add default data in DB
Pre-fill the DB with a RBAC policy
```bash
cd ${MOON_HOME}/moon_interface/tests/apitests
python3 populate_default_values.py scenario/ rbac.py
```
