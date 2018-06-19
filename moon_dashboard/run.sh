#!/bin/sh
# sudo docker run -ti --rm -p 8000:8000 -e MANAGER_HOST=localhost -e MANAGER_PORT=30001 -e KEYSTONE_HOST=localhost -e KEYSTONE_PORT=30005 moonplatform/dashboard:dev

CONSTANT_FILE=/root/horizon/openstack_dashboard/dashboards/moon/static/moon/js/moon.module.js

sed "s/{{MANAGER_HOST}}/$MANAGER_HOST/g" -i $CONSTANT_FILE
sed "s/{{MANAGER_PORT}}/$MANAGER_PORT/g" -i $CONSTANT_FILE
sed "s/{{KEYSTONE_HOST}}/$KEYSTONE_HOST/g" -i $CONSTANT_FILE
sed "s/{{KEYSTONE_PORT}}/$KEYSTONE_PORT/g" -i $CONSTANT_FILE

cd /root/horizon

LOCAL_SETTINGS=/root/horizon/openstack_dashboard/local/local_settings.py
sed "s/OPENSTACK_HOST = \"127.0.0.1\"/OPENSTACK_HOST = \"${OPENSTACK_HOST}\"/" -i $LOCAL_SETTINGS
sed "s#OPENSTACK_KEYSTONE_URL = \"http:\/\/%s:5000\/v2.0\" % OPENSTACK_HOST#OPENSTACK_KEYSTONE_URL = \"${OPENSTACK_KEYSTONE_URL}\"#" -i $LOCAL_SETTINGS

echo -----------------
grep OPENSTACK_HOST $LOCAL_SETTINGS
grep OPENSTACK_KEYSTONE_URL LOCAL_SETTINGS
echo -----------------

echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ $CONSTANT_FILE"
cat $CONSTANT_FILE
echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

tox -e runserver -- 0.0.0.0:8000