#!/usr/bin/env bash

if [ $# -eq 1 ]; then cd $1; fi

# ==========================================================
# test for OpenStack/Moon API through moonclient cli

python run_tests.py

# ==========================================================
# test for OpenStack OpenDaylight identity federation

# create tenant, user, and password in OpenStack/moon
# use the created tenant, user, password to access OpenDaylight
