#!/usr/bin/env bash

service apache2 start

sed "s/{{MANAGER_HOST}}/$MANAGER_HOST/g" -i /root/static/app/moon.constants.js
sed "s/{{MANAGER_PORT}}/$MANAGER_PORT/g" -i /root/static/app/moon.constants.js
sed "s/{{KEYSTONE_HOST}}/$KEYSTONE_HOST/g" -i /root/static/app/moon.constants.js
sed "s/{{KEYSTONE_PORT}}/$KEYSTONE_PORT/g" -i /root/static/app/moon.constants.js

echo "--------------------------"
cat /root/static/app/moon.constants.js
echo "--------------------------"

gulp delivery
cp -rv /root/delivery/* /var/www/html

tail -f /var/log/apache2/error.log
