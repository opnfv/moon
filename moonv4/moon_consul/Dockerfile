# Pull base image.
FROM ubuntu:latest

ENV DB_URL="mysql+pymysql://moon:p4sswOrd1@db/moon"
ENV DB_DRIVER=sql
ENV TRANSPORT_URL="rabbit://moon:p4sswOrd1@messenger:5672/moon"
ENV DOCKER_URL="unix://var/run/docker.sock"
ENV SLAVE_NAME=
ENV MASTER_URL=
ENV MASTER_LOGIN=
ENV MASTER_PASSWORD=
ENV INTERFACE_PORT=8080
ENV CONSUL_HOST="172.88.88.88"
ENV CONSUL_PORT=88
ENV KEYSTONE_URL="http://keystone:5000/v3"
ENV KEYSTONE_USER=admin
ENV KEYSTONE_PASSWORD=p4ssw0rd
ENV KEYSTONE_DOMAIN=default
ENV KEYSTONE_PROJECT=admin
ENV KEYSTONE_CHECK_TOKEN=False
ENV KEYSTONE_SERVER_CRT=False
ENV PLUGIN_CONTAINERS="asteroide/authz:latest,asteroide/session:latest"
ENV COMPONENTS_PORT_START=38001

RUN apt-get update && apt-get install python3.5 python3-pip -y

RUN pip3 install pip --upgrade
#RUN pip3 install moon_db

ADD . /root

WORKDIR /root/
RUN pip3 install -r requirements.txt
RUN pip3 install .
EXPOSE ${CONSUL_PORT}

CMD ["python3", "-m", "moon_consul"]