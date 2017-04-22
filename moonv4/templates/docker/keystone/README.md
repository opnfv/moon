# Keystone container

## How to use

```bash
docker build --build-arg https_proxy=http://proxy:3128 --build-arg http_proxy=http://proxy:3128 -t keystone:mitaka .
docker run -dti --net moon --name keystone --hostname=keystone -e DB_HOST=db -e DB_PASSWORD_ROOT=my_password -p 35357:35357 -p 5000:5000 keystone:mitaka
```