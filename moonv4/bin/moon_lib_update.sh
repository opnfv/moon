#!/usr/bin/env bash

# usage: moon_update.sh {build,upload,copy} {python_moondb,python_moonutilities} <GPG_ID>

CMD=$1
COMPONENT=$2
GPG_ID=$3

VERSION=${COMPONENT}-$(grep __version__ ${COMPONENT}/${COMPONENT}/__init__.py | cut -d "\"" -f 2)

cd ${COMPONENT}

python3 setup.py sdist bdist_wheel

if [ "$CMD" = "upload" ]; then
    # Instead of "A0A96E75", use your own GPG ID
    rm dist/*.asc 2>/dev/null
    gpg --detach-sign -u "${GPG_ID}" -a dist/${VERSION}-py3-none-any.whl
    gpg --detach-sign -u "${GPG_ID}" -a dist/${VERSION/_/-}.tar.gz
    twine upload dist/${VERSION}-py3-none-any.whl dist/${VERSION}-py3-none-any.whl.asc
    twine upload dist/${VERSION/_/-}.tar.gz dist/${VERSION/_/-}.tar.gz.asc
fi

rm -f ../moon_manager/dist/${COMPONENT}*
rm -f ../moon_orchestrator/dist/${COMPONENT}*
rm -f ../moon_wrapper/dist/${COMPONENT}*
rm -f ../moon_interface/dist/${COMPONENT}*
rm -f ../moon_authz/dist/${COMPONENT}*


if [ "$CMD" = "copy" ]; then
    mkdir -p ../moon_manager/dist/ 2>/dev/null
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_manager/dist/
    mkdir -p ../moon_orchestrator/dist/ 2>/dev/null
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_orchestrator/dist/
    mkdir -p ../moon_wrapper/dist/ 2>/dev/null
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_wrapper/dist/
    mkdir -p ../moon_interface/dist/ 2>/dev/null
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_interface/dist/
    mkdir -p ../moon_authz/dist/ 2>/dev/null
    cp -v dist/${VERSION}-py3-none-any.whl ../moon_authz/dist/
fi

