#!/usr/bin/env bash

hug -m moon_engine.server -p 10000 gunicorn.cfg
