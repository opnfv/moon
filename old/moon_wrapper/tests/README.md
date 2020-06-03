# Tests

## Python Unit Test for moon_db

- launch Docker for Python unit tests


    cd ${MOON_HOME}/moonv4/moon_db/
    docker run -ti --volume ${PWD}:/data asteroide/moon_tests


## Build and upload python packages

- build python packages


    python setup.py sdist bdist_wheel


- upload moon_db to PIP
    
    
    python setup.py upload


or 


    gpg --detach-sign -u "${GPG_ID}" -a dist/moon_db-X.Y.Z-py3-none-any.whl
    gpg --detach-sign -u "${GPG_ID}" -a dist/moon_db-X.Y.Z.tar.gz
    twine upload dist/moon_db-X.Y.Z-py3-none-any.whl dist/moon_db-X.Y.Z-py3-none-any.whl.asc
    twine upload dist/moon_db-X.Y.Z.tar.gz dist/moon_db-X.Y.Z.tar.gz.asc



