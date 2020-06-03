# python-moonutilities Package
This package contains the core module for the Moon project.
It is designed to provide authorization feature to all OpenStack components.

For any other information, refer to the parent project:

    https://git.opnfv.org/moon

python-moonutilities is a common Python lib for other Moon Python packages

## Build
### Build Python Package
```bash
cd ${MOON_HOME}/python_moonutilities
python3 setup.py sdist bdist_wheel
```

### Push Python Package to PIP
```bash
cd ${MOON_HOME}/python_moonutilities
gpg --detach-sign -u "${GPG_ID}" -a dist/python_moonutilities-X.Y.Z-py3-none-any.whl
gpg --detach-sign -u "${GPG_ID}" -a dist/python_moonutilities-X.Y.Z.tar.gz
twine upload dist/python_moonutilities-X.Y.Z-py3-none-any.whl dist/python_moonutilities-X.Y.Z-py3-none-any.whl.asc
twine upload dist/python_moonutilities-X.Y.Z.tar.gz dist/python_moonutilities-X.Y.Z.tar.gz.asc
```

## Test
### Python Unit Test
launch Docker for Python unit tests
```bash
cd ${MOON_HOME}/python_moonutilities
docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest
```
