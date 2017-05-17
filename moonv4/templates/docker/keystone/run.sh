#!/usr/bin/env bash

MY_HOSTNAME=localhost

echo DB_HOST=$DB_HOST
echo DB_DATABASE=$DB_DATABASE
echo RABBIT_NODE=$RABBIT_NODE
echo RABBIT_NODE=$[RABBIT_NODE]
echo INTERFACE_HOST=$INTERFACE_HOST

sed "s/#admin_token = <None>/admin_token=$ADMIN_TOKEN/g" -i /etc/keystone/keystone.conf
sed "s/connection = sqlite:\/\/\/\/var\/lib\/keystone\/keystone.db/connection = $DB_CONNECTION:\/\/$DB_USER:$DB_PASSWORD@$DB_HOST\/$DB_DATABASE/g" -i /etc/keystone/keystone.conf
sed "s/#driver = sql/driver = $DB_DRIVER/g" -i /etc/keystone/keystone.conf

cat << EOF | tee -a /etc/keystone/keystone.conf
[cors]
allowed_origin = $INTERFACE_HOST
max_age = 3600
allow_methods = GET,POST,PUT,DELETE
allow_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Custom-Header
expose_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma,X-Custom-Header
EOF

mysql -h $DB_HOST -u$DB_USER_ROOT -p$DB_PASSWORD_ROOT <<EOF
CREATE DATABASE $DB_DATABASE DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON $DB_DATABASE.* TO '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL ON $DB_DATABASE.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
EOF

#rabbitmqctl -n rabbit@$RABBIT_NODE add_user openstack password
#rabbitmqctl -n rabbit@$RABBIT_NODE set_permissions openstack ".*" ".*" ".*"

cat << EOF | tee /etc/apache2/sites-available/wsgi-keystone.conf
Listen 5000
Listen 35357

<VirtualHost *:5000>
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-public
    WSGIScriptAlias / /usr/bin/keystone-wsgi-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>

<VirtualHost *:35357>
    WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-admin
    WSGIScriptAlias / /usr/bin/keystone-wsgi-admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>

EOF

a2ensite wsgi-keystone

service keystone stop
echo "manual" | tee /etc/init/keystone.override

service apache2 restart

netstat -tanpeo

export http_proxy=
export https_proxy=

keystone-manage db_sync

keystone-manage bootstrap \
    --bootstrap-password ${ADMIN_PASSWORD} \
    --bootstrap-username admin \
    --bootstrap-project-name admin \
    --bootstrap-role-name admin \
    --bootstrap-service-name keystone \
    --bootstrap-region-id Orange \
    --bootstrap-admin-url http://localhost:35357 \
    --bootstrap-public-url http://localhost:5000 \
    --bootstrap-internal-url http://localhost:5000


export OS_USERNAME=admin
export OS_PASSWORD=${ADMIN_PASSWORD}
export OS_REGION_NAME=Orange
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://localhost:5000/v3
export OS_DOMAIN_NAME=Default

openstack project create --description "Service Project" demo
openstack role create user
openstack role add --project demo --user demo user

echo -e "\n Project list:"
openstack project list

echo -e "\n Users list:"
openstack user list

echo -e "\n Roles list:"
openstack role list

echo -e "\n Service list:"
openstack service list

echo -e "\n Endpoint list:"
openstack endpoint list --long


tail -f /var/log/apache2/keystone.log