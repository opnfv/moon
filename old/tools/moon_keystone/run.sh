#!/usr/bin/env bash

MY_HOSTNAME=localhost

echo DB_HOST=$DB_HOST
echo DB_DATABASE=$DB_DATABASE
echo RABBIT_NODE=$RABBIT_NODE
echo RABBIT_NODE=$[RABBIT_NODE]
echo INTERFACE_HOST=$INTERFACE_HOST

sed "s/#admin_token = <None>/admin_token=$ADMIN_TOKEN/g" -i /etc/keystone/keystone.conf
sed "s/#connection = <None>/connection = $DB_CONNECTION:\/\/$DB_USER:$DB_PASSWORD@$DB_HOST\/$DB_DATABASE/g" -i /etc/keystone/keystone.conf

cat << EOF | tee -a /etc/keystone/keystone.conf
[cors]
allowed_origin = $INTERFACE_HOST
max_age = 3600
allow_methods = POST,GET,DELETE
EOF

until echo status | mysql -h${DB_HOST} -u${DB_USER_ROOT} -p${DB_PASSWORD_ROOT}; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "Mysql is up - executing command"

mysql -h $DB_HOST -u$DB_USER_ROOT -p$DB_PASSWORD_ROOT <<EOF
CREATE DATABASE $DB_DATABASE DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON $DB_DATABASE.* TO '$DB_USER'@'%' IDENTIFIED BY '$DB_PASSWORD';
GRANT ALL ON $DB_DATABASE.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASSWORD';
EOF

keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
keystone-manage credential_setup --keystone-user keystone --keystone-group keystone

su -s /bin/sh -c "keystone-manage db_sync" keystone

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


service apache2 start

export OS_USERNAME=admin
export OS_PASSWORD=${ADMIN_PASSWORD}
export OS_REGION_NAME=Orange
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://localhost:5000/v3
export OS_DOMAIN_NAME=Default
export OS_IDENTITY_API_VERSION=3

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
openstack endpoint list


tail -f /var/log/apache2/keystone.log