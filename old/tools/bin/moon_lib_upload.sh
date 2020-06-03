#!/usr/bin/env bash

# usage: moon_update.sh <GPG_ID>

COMPONENT=$(basename $(pwd))
GPG_ID=$1

if [ -f setup.py ]; then
    echo
else
    echo "Not a python package"
    exit 1
fi

VERSION=${COMPONENT}-$(grep __version__ ${COMPONENT}/__init__.py | cut -d "\"" -f 2)

python3 setup.py sdist bdist_wheel

echo $COMPONENT
echo $VERSION

# Instead of "A0A96E75", use your own GPG ID
rm dist/*.asc 2>/dev/null
gpg --detach-sign -u "${GPG_ID}" -a dist/${VERSION}-py3-none-any.whl
gpg --detach-sign -u "${GPG_ID}" -a dist/${VERSION/_/-}.tar.gz
twine upload dist/${VERSION}-py3-none-any.whl dist/${VERSION}-py3-none-any.whl.asc
twine upload dist/${VERSION/_/-}.tar.gz dist/${VERSION/_/-}.tar.gz.asc
