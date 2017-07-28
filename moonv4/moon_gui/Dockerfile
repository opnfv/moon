FROM ubuntu:latest

RUN apt update && apt install nodejs nodejs-legacy npm -y
RUN npm install --global gulp-cli

ADD . /root
WORKDIR /root/
RUN npm install
RUN gulp delivery

CMD ["gulp", "webServerDelivery"]