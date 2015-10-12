#!/usr/bin/env bash

# as user demo
. openrc demo

# create authz intraextension
moon intraextension add policy_mls_authz test_authz

# create admin intraextension
moon intraextension add policy_rbac_admin test_admin

# create tenant
moon tenant add --authz xxx --admin xxx demo

# select the authz tenant
moon intraextension select `test_authz_uuid`

# check that moon blocks modification of object assignments
moon object assignment add `vm1_uuid` `object_security_level_uuid` `high_uuid`

# as user admin
. openrc admin

# select the admin intraextension
moon intraextension select `test_admin_uuid`

# add write permission to the dev_role user for assignment table
moon rule add `rbac_rule_uuid` [`dev_role_uuid`, `write_uuid`, `authz.assignment`]

# as user demo
. openrc demo

# select the authz intraextension
moon intraextension select `test_authz_uuid`

# check that moon authorizes modification of rule table by demo
moon object assignment add `vm1_uuid` `object_security_level_uuid` `high_uuid`
