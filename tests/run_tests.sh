#!/usr/bin/env bash

# ==========================================================
# test for OpenStack/Moon API through moonclient cli

tenant_net_name=public

openstack project list

moon intraextension list

NET_ID=$(nova net-list | grep $tenant_net_name | awk '{print $2}')

echo \* Creating and booting a sample VM ...
nova boot --flavor m1.tiny --image cirros-0.3.3-x86_64 --security-groups default --nic net-id=$NET_ID --poll moontest

moon intraextension add --policy_model policy_authz --description "test" ie_test

IE_ID=$(moon intraextension list | grep ie_test | awk '{print $2}')

nova list

moon tenant add admin

TENANT_ID=$(moon tenant list | grep "Admin Project" | awk '{print $2}')

moon tenant set --authz ${IE_ID} ${TENANT_ID}

VM_ID=$(nova list | grep moontest | grep ACTIVE | awk '{print $2}')
echo \*\* Nova VM ID is ${VM_ID}

echo \!\!\! Error is normal here
nova pause ${VM_ID}
echo Error is normal here \!\!\!

moon intraextension select ${IE_ID}
echo \*\* Intraextension ID is ${IE_ID}

echo \*\* Subject list
moon subject list

echo \*\* Object list
moon object list

moon object add ${VM_ID}

OBJ_ID=$(moon object list | grep ${VM_ID} | awk '{print $2}')
echo \*\* Moon Object ID is ${OBJ_ID}

OBJ_CAT_ID=$(moon object category list | grep object_security_level | awk '{print $2}')
echo \*\* Category object_security_level ID is ${OBJ_CAT_ID}

OBJ_SCOPE_ID=$(moon object scope list ${OBJ_CAT_ID} | grep low | awk '{print $2}')
echo \*\* Scope low ID is ${OBJ_SCOPE_ID}

moon object assignment add ${OBJ_ID} ${OBJ_CAT_ID} ${OBJ_SCOPE_ID}

moon aggregation algorithm show
ALGO_ID=$(moon aggregation algorithm list | grep one_true | awk '{print $2}')
moon aggregation algorithm set ${ALGO_ID}
moon aggregation algorithm show

nova pause ${VM_ID}

echo \*\* There must be NO error here

nova list

moon log

echo \*\* Deleting test VM
nova delete ${VM_ID}

echo \* Testing Swift \(may take time... be patient\)

echo \!\!\! Error is normal here
swift list
echo Error is normal here \!\!\!

AUTH_ID=$(swift auth | grep STORAGE_URL | cut -d "/" -f "5")
echo \*\* Auth_id is ${AUTH_ID}

echo \*\* Add ${AUTH_ID} object
moon object add ${AUTH_ID}

OBJ_ID=$(moon object list | grep ${AUTH_ID} | awk '{print $2}')
echo \*\*\* Moon Object ID is ${OBJ_ID}

OBJ_CAT_ID=$(moon object category list | grep object_security_level | awk '{print $2}')
echo \*\*\* Category object_security_level ID is ${OBJ_CAT_ID}

OBJ_SCOPE_ID=$(moon object scope list ${OBJ_CAT_ID} | grep low | awk '{print $2}')
echo \*\*\* Scope low ID is ${OBJ_SCOPE_ID}

moon object assignment add ${OBJ_ID} ${OBJ_CAT_ID} ${OBJ_SCOPE_ID}

echo \*\* Add get_account_details action

moon action add get_account_details
ACT_ID=$(moon action list | grep "get_account_details" | awk '{print $2}')

ACT_CAT_ACCESS_ID=$(moon action category list | grep "access" |  awk '{print $2}')
ACT_CAT_RESOURCE_ID=$(moon action category list | grep "resource_action" |  awk '{print $2}')

ACT_SCOPE_ACCESS_ID=$(moon action scope list ${ACT_CAT_ACCESS_ID} | grep "read" |  awk '{print $2}')
ACT_SCOPE_RESOURCE_ID=$(moon action scope list ${ACT_CAT_RESOURCE_ID} | grep "storage_access" |  awk '{print $2}')

moon action assignment add ${ACT_ID} ${ACT_CAT_ACCESS_ID} ${ACT_SCOPE_ACCESS_ID}
moon action assignment add ${ACT_ID} ${ACT_CAT_RESOURCE_ID} ${ACT_SCOPE_RESOURCE_ID}

SUBMETARULE_ID=$(moon submetarule show | grep "mls_rule" |  awk '{print $2}')

moon rule add ${SUBMETARULE_ID} "high,storage_access,low"

echo \*\* Swift must be OK here
swift list

echo \* Deleting intraextension
moon tenant set --authz "" ${TENANT_ID}

moon intraextension delete ${IE_ID}


# ==========================================================
# test for OpenStack OpenDaylight identity federation

# create tenant, user, and password in OpenStack/moon
# use the created tenant, user, password to access OpenDaylight
