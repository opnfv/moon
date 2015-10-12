#!/bin/sh

# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.


PROG=moon
OS_TENANT_NAME=demo
DEMO_USER=$(keystone user-list | awk '/ demo / {print $2}')

# must be authenticated with Keystone
# ie. : "cd ~/devstack; . openrc admin"

function test_cmd {
    echo -e "\033[33m$PROG $1\033[m"
    $PROG $1 | tee /tmp/_
    if [ $? != 0 ]; then
        echo -e "\033[31mError for test \"$1\" \033[m"
        exit 1
    fi
}

test_cmd "intraextension list"
test_cmd "intraextension add --policy_model policy_rbac func_test"
uuid=$(cat /tmp/_ | cut -d " " -f 3)
test_cmd "intraextension tenant set $uuid $OS_TENANT_NAME"
test_cmd "intraextension show $uuid"

test_cmd "subjects list"
test_cmd "subjects add $DEMO_USER"
test_cmd "subjects list"

test_cmd "objects list"
test_cmd "objects add my_obj"
test_cmd "objects list"

test_cmd "actions list"
test_cmd "actions add my_action"
test_cmd "actions list"

# Category

test_cmd "subject categories list"
test_cmd "subject categories add my_cat"
test_cmd "subject categories list"

test_cmd "object categories list"
test_cmd "object categories add my_cat"
test_cmd "object categories list"

test_cmd "action categories list"
test_cmd "action categories add my_cat"
test_cmd "action categories list"

# Category scope

test_cmd "subject category scope list"
test_cmd "subject category scope add my_cat my_scope"
test_cmd "subject category scope list"

test_cmd "object category scope list"
test_cmd "object category scope add my_cat my_scope"
test_cmd "object category scope list"

test_cmd "action category scope list"
test_cmd "action category scope add my_cat my_scope"
test_cmd "action category scope list"

# Assignments

test_cmd "subject assignments list"
test_cmd "subject assignments add $DEMO_USER my_cat my_scope"
test_cmd "subject assignments list"

test_cmd "object assignments list"
test_cmd "object assignments add my_obj my_cat my_scope"
test_cmd "object assignments list"

test_cmd "action assignments list"
test_cmd "action assignments add my_action my_cat my_scope"
test_cmd "action assignments list"

# Sub meta rules

test_cmd "aggregation algorithms list"
test_cmd "aggregation algorithm show"
test_cmd "aggregation algorithm set test_aggregation"
test_cmd "aggregation algorithm show"
test_cmd "submetarule show"
test_cmd "submetarule set relation_super subject_security_level,my_cat computing_action,my_cat object_security_level,my_cat"
test_cmd "submetarule show"
test_cmd "submetarule relation list"

# Rules

test_cmd "rules list"
test_cmd "rules add relation_super high,my_scope,vm_access,my_scope,high,my_scope"
test_cmd "rules delete relation_super high,my_scope,vm_access,my_scope,high,my_scope"

#Delete all
test_cmd "subject assignments delete $DEMO_USER my_cat my_scope"
test_cmd "subject assignments list"
test_cmd "object assignments delete my_obj my_cat my_scope"
test_cmd "object assignments list"
test_cmd "action assignments delete my_action my_cat my_scope"
test_cmd "action assignments list"

test_cmd "subject category scope delete my_cat my_scope"
test_cmd "subject category scope list"
test_cmd "object category scope delete my_cat my_scope"
test_cmd "object category scope list"
test_cmd "action category scope delete my_cat my_scope"
test_cmd "action category scope list"

test_cmd "subjects delete $DEMO_USER"
test_cmd "subjects list"
test_cmd "objects delete my_obj"
test_cmd "objects list"
test_cmd "actions delete my_action"
test_cmd "actions list"
test_cmd "subject categories delete my_cat"
test_cmd "subject categories list"
test_cmd "object categories delete my_cat"
test_cmd "object categories list"
test_cmd "action categories delete my_cat"
test_cmd "action categories list"


test_cmd "intraextension delete $uuid"