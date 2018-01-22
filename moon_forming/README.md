# Moon Forming 
moon_forming is a container to automatize the configuration of the Moon platform

## Run
```bash
docker run wukongsun/moon_forming:latest
```

## Consul
The Moon platform is already configured after the installation.
If you want to see or modify the configuration, go with a web browser 
to the following page: `http://localhost:30006`.

With the consul server, you can update the configuration in the `KEY/VALUE` tab.
There are some configuration items, lots of them are only read when a new K8S pod is started
and not during its life cycle.

**WARNING: some confidential information are put here in clear text.
This is a known security issue.**

### Keystone
If you have your own Keystone server, you can point Moon to your Keystone in the 
`openstack/keystone` element: `http://localhost:30005/ui/#/dc1/kv/openstack/keystone/edit`.
This configuration element is read every time Moon need it, specially when adding users.

### Database
The database can also be modified through: `http://localhost:30005/ui/#/dc1/kv/database/edit`.

**WARNING: the password is in clear text, this is a known security issue.**

If you want to use your own database server, change the configuration:

    {"url": "mysql+pymysql://my_user:my_secret_password@my_server/moon", "driver": "sql"}

Then you have to rebuild the database before using it. 
This can be done with the following commands:
```bash
kubectl delete -f $MOON_HOME/tools/moon_kubernetes/templates/moon_forming.yaml
kubectl create -f $MOON_HOME/tools/moon_kubernetes/templates/moon_forming.yaml
```

## Functional tests

```bash
cd $MOON_HOME/moon_manager
bash ../tests/functional/run_tests_for_component.sh
```
