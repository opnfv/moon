#!/usr/bin/env bash

# TODO: wait for consul
python3 /root/conf2consul.py /etc/moon/moon.conf

# TODO: wait for database
moon_db_manager upgrade