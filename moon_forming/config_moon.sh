#!/usr/bin/env bash

populate_args=$*

echo "Waiting for Consul (http://consul:8500)"
while ! python -c "import requests; req = requests.get('http://consul:8500')" 2>/dev/null ; do
    sleep 5 ;
    echo -n "."
done
echo "."
echo "Consul (http://consul:8500) is up."

python3 /root/conf2consul.py /etc/moon/moon.conf

echo "Waiting for DB (tcp://db:3306)"
while ! python -c "import socket, sys; s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(('db', 3306)); sys.exit(0)" 2>/dev/null ; do
    sleep 5 ;
    echo -n "."
done
echo "."
echo "Database (http://db:3306) is up."

moon_db_manager upgrade

echo "Waiting for Keystone (http://keystone:5000)"
while ! python -c "import requests; req = requests.get('http://keystone:5000')" 2>/dev/null ; do
    sleep 5 ;
    echo -n "."
done
echo "."
echo "Keystone (http://keystone:5000) is up."

echo "Waiting for Manager (http://manager:8082)"
while ! python -c "import requests; req = requests.get('http://manager:8082')" 2>/dev/null ; do
    sleep 5 ;
    echo -n "."
done
echo "."
echo "Manager (http://manager:8082) is up."
