#!/usr/bin/env bash

# TODO: wait for consul
python3 /root/conf2consul.py /etc/moon/moon.conf

# TODO: wait for database
moon_db_manager upgrade

echo "Waiting for manager (http://manager:8082)"
while ! python -c "import requests; req = requests.get('http://manager:8082')" 2>/dev/null ; do
    sleep 5 ;
    echo "."
done

echo "Manager (http://manager:8082) is up."

cd /root
python3 populate_default_values.py -v /root/conf/rbac.py
python3 populate_default_values.py -v /root/conf/mls.py
