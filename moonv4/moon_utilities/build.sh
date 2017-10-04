

VERSION=moon_utilities-1.2.0

python3 setup.py sdist bdist_wheel

rm dist/*.asc

gpg --detach-sign -u "A0A96E75" -a dist/${VERSION}-py3-none-any.whl
gpg --detach-sign -u "A0A96E75" -a dist/${VERSION}.linux-x86_64.tar.gz

if [ "$1" = "upload" ]; then
    twine upload dist/${VERSION}-py3-none-any.whl dist/${VERSION}-py3-none-any.whl.asc
    twine upload dist/${VERSION}.linux-x86_64.tar.gz dist/${VERSION}.linux-x86_64.tar.gz.asc
fi

cp dist/${VERSION}-py3-none-any.whl ../moon_orchestrator/dist/
cp dist/${VERSION}-py3-none-any.whl ../moon_router/dist/
cp dist/${VERSION}-py3-none-any.whl ../moon_interface/dist/
cp dist/${VERSION}-py3-none-any.whl ../moon_manager/dist/
cp dist/${VERSION}-py3-none-any.whl ../moon_authz/dist/
