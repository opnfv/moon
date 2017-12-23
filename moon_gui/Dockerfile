FROM ubuntu:latest

RUN apt update && apt install git nodejs nodejs-legacy npm apache2 -y
RUN npm install --global gulp-cli

ENV MANAGER_HOST="127.0.0.1"
ENV MANAGER_PORT=8080
ENV KEYSTONE_HOST="127.0.0.1"
ENV KEYSTONE_PORT=5000

ADD . /root
WORKDIR /root/

RUN npm install

#CMD ["gulp"]
#CMD ["gulp", "webServerDelivery"]
CMD ["sh", "/root/run.sh"]