#!/usr/bin/env bash

# as user admin

# create authz intraextension
moon intraextension add policy_mls_authz test_authz

# create admin intraextension
moon intraextension add policy_rbac_admin test_admin

# create tenant
moon tenant add --authz xxx --admin xxx demo

# select the authz tenant
moon intraextension select `test_authz_uuid`

# create a VM (vm1) in OpenStack
nova create vm1.....

# add corresponding object in moon
moon object add vm1

# check that moon blocks the vm1 manipulatin
nova vm1 suspend ....

# add object assignment for vm1
moon object assignment `vm1_uuid` `object_security_level_uuid` `high_uuid`

# check now moon block the manipulation of vm1
nova vm1 suspend ....

# del object assignment for servers
moon object assignment del `vm1_uuid` `object_security_level_uuid` `high_uuid`

# add object assignment for servers
moon object assignment add `vm1_uuid` `object_security_level_uuid` `low_uuid`

# check now moon unblock the manipulation of vm1
nova vm1 suspend ....