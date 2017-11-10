#!/usr/bin/env bash

VERSION=moon_db-$(grep __version__ moon_db/__init__.py | cut -d "\"" -f 2)

python3 setup.py sdist bdist_wheel

rm dist/*.asc 2>/dev/null

gpg --detach-sign -u "A0A96E75" -a dist/${VERSION}-py3-none-any.whl
gpg --detach-sign -u "A0A96E75" -a dist/${VERSION}.tar.gz

if [ "$1" = "upload" ]; then
    twine upload dist/${VERSION}-py3-none-any.whl dist/${VERSION}-py3-none-any.whl.asc
    twine upload dist/${VERSION}.tar.gz dist/${VERSION}.tar.gz.asc
    rm -f ../moon_orchestrator/dist/moon_db*
    rm -f ../moon_interface/dist/moon_db*
    rm -f ../moon_manager/dist/moon_db*
    rm -f ../moon_authz/dist/moon_db*
    rm -f ../moon_wrapper/dist/moon_db*
fi

if [ "$1" = "copy" ]; then
    mkdir -p ../moon_orchestrator/dist/ 2>/dev/null
    rm -f ../moon_orchestrator/dist/moon_db*
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_orchestrator/dist/
    mkdir -p ../moon_interface/dist/ 2>/dev/null
    rm -f ../moon_interface/dist/moon_db*
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_interface/dist/
    mkdir -p ../moon_manager/dist/ 2>/dev/null
    rm -f ../moon_manager/dist/moon_db*
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_manager/dist/
    mkdir -p ../moon_authz/dist/ 2>/dev/null
    rm -f ../moon_authz/dist/moon_db*
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_authz/dist/
    mkdir -p ../moon_wrapper/dist/ 2>/dev/null
    rm -f ../moon_wrapper/dist/moon_db*
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_wrapper/dist/
fi
