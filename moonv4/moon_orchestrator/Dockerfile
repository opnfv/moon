FROM ubuntu:latest

ENV CONSUL_HOST=consul
ENV CONSUL_PORT=8500

RUN apt update && apt install python3.5 python3-pip python3-mysql.connector -y
RUN pip3 install pip --upgrade

ADD . /root
WORKDIR /root/
RUN pip3 install -r requirements.txt --upgrade
RUN pip3 install . --upgrade

CMD ["python3", "bootstrap.py"]