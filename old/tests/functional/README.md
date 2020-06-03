# Moon Functional Test

[Test Platform Setup](../../tools/moon_kubernetes/README.md)


### Pod Functional Test
Launch functional [test scenario](tests/functional/scenario_enabled) : 
```bash
sudo pip install python_moonclient --upgrade
cd $MOON_HOME/tests/functional/scenario_tests
moon_create_pdp --consul-host=$MOON_HOST --consul-port=30005 -v rbac_large.py
moon_get_keystone_project --consul-host=$MOON_HOST --consul-port=30005 
moon_get_pdp --consul-host=$MOON_HOST --consul-port=30005 
moon_map_pdp_to_project "<pdp_id>" "<keystone_project_id>"
moon_send_authz_to_wrapper --consul-host=$MOON_HOST --consul-port=30005 --authz-host=$WRAPPER_HOST --authz-port=$WRAPPER_PORT -v rbac_large.py
```

To retrieve the wrapper information, use the following command:
```bash
kubectl get -n moon services | grep wrapper
```

Launch functional tests:
```bash
cd $MOON_HOME
sudo bash $TARGET_MODULE/tests/functional_pod/run_functional_tests.sh
```
