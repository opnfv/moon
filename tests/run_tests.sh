#!/usr/bin/env bash

# ==========================================================
# test for OpenStack/Moon API through moonclient cli

python run_tests.py

# ==========================================================
# test for OpenStack OpenDaylight identity federation

# create tenant, user, and password in OpenStack/moon
# use the created tenant, user, password to access OpenDaylight
