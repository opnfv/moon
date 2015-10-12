#!/usr/bin/env bash

# as user admin

# create authz intraextension
moon intraextension add policy_mls_authz test_authz

# create admin intraextension
moon intraextension add policy_rbac_admin test_admin

# create tenant
moon tenant add --authz xxx --admin xxx `demo`

# check that now moon authorizes the manipulation list_servers
nova list

# select the authz intraextension
moon intraextension select `test_authz_uuid`

# del object assignment for servers
moon object assignment del `servers_uuid` `object_security_level_uuid` `low_uuid`

# add object assignment for servers
moon object assignment add `servers_uuid` `object_security_level_uuid` `high_uuid`

# check now moon block the manipulation list_servers
nova list

# del object assignment for servers
moon object assignment del `servers_uuid` `object_security_level_uuid` `high_uuid`

# add object assignment for servers
moon object assignment add `servers_uuid` `object_security_level_uuid` `low_uuid`