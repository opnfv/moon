# Keystone container

## build keystone image

without proxy: 
```bash
docker build -t keystone:mitaka .
```

with a proxy:
```bash
docker build --build-arg https_proxy=http://proxy:3128 --build-arg http_proxy=http://proxy:3128 -t keystone:mitaka .
```


### access to the container
```bash
docker container exec -ti keystone /bin/bash
export OS_USERNAME=admin
export OS_PASSWORD=p4ssw0rd
export OS_REGION_NAME=Orange
export OS_TENANT_NAME=admin
export OS_AUTH_URL=http://localhost:5000/v3
export OS_DOMAIN_NAME=Default
openstack project list
```