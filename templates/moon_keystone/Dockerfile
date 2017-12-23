FROM ubuntu:zesty

ENV ADMIN_TOKEN=p4ssw0rd
ENV ADMIN_PASSWORD=p4ssw0rd
ENV DB_CONNECTION="mysql+pymysql"
ENV DB_DRIVER=sql
ENV DB_HOST=localhost
ENV DB_DATABASE=keystonedb
ENV DB_USER=keystone
ENV DB_PASSWORD=p4ssw0rd
ENV DB_USER_ROOT=root
ENV DB_PASSWORD_ROOT=p4sswOrd1
ENV RABBIT_NODE=server
ENV INTERFACE_HOST="http://localhost:3001"

RUN apt update && apt install apache2 rabbitmq-server keystone python-openstackclient libapache2-mod-wsgi mysql-client -y

# RUN apt update && apt install iputils-ping net-tools -y

ADD run.sh /root

EXPOSE 35357
EXPOSE 5000

CMD ["/bin/bash", "/root/run.sh"]