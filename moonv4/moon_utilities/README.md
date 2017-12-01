# Moon Python Utilities Package
This package contains the core module for the Moon project
It is designed to provide authorization features to all OpenStack components.

For any other information, refer to the parent project:

    https://git.opnfv.org/moon

moon_utilities is a common Python lib for other Moon Python packages

## Build
### Build Python Package
- `cd moon_utilities`
- `python3 setup.py sdist bdist_wheel`

### Push Python Package to PIP

## Test
### Python Unit Test
- launch Docker for Python unit tests
    - `cd moon_utilities`
    - `docker run --rm --volume $(pwd):/data wukongsun/moon_python_unit_test:latest`

