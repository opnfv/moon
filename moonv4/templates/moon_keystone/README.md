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


## set up an execution environment

### clean up if necessary
```bash
docker container rm -f $(docker ps -a | grep moon | cut -d " " -f 1) 2>/dev/null
docker container rm -f messenger db keystone 2>/dev/null
```
 
### create a network
```bash
docker network create -d bridge --subnet=172.18.0.0/16 --gateway=172.18.0.1 moon
```

### Start RabbitMQ
TODO: use our own container 
```bash
docker container run -dti --net=moon --hostname messenger --name messenger -e RABBITMQ_DEFAULT_USER=moon -e RABBITMQ_DEFAULT_PASS=p4sswOrd1 -e RABBITMQ_NODENAME=rabbit@messenger -e RABBITMQ_DEFAULT_VHOST=moon -e RABBITMQ_HIPE_COMPILE=1 -p 5671:5671 -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```


### Start MySQL server
TODO: user our own containter
```bash
docker container run -dti --net=moon --hostname db --name db -e MYSQL_ROOT_PASSWORD=p4sswOrd1 -e MYSQL_DATABASE=moon -e MYSQL_USER=moon -e MYSQL_PASSWORD=p4sswOrd1 -p 3306:3306 mysql:latest
```

## launch a Keystone container
TODO: user our own containter
```bash
docker container run -dti --net moon --hostname keystone  --name keystone  -e DB_HOST=db -e DB_PASSWORD_ROOT=p4sswOrd1 -p 35357:35357 -p 5000:5000 keystone:mitaka
```

## check
### log
```bash
docker logs keystone -f
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