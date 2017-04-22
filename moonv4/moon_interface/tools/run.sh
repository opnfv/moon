#!/usr/bin/env bash

http_proxy= /usr/bin/python3 /home/vdsq3226/projets/opnfv/opnfv-moon/moon_interface/tools/api2rst.py
pandoc api.rst --toc -o api.pdf
evince api.pdf
