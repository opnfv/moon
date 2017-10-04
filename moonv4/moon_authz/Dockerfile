FROM ubuntu:latest

ENV UUID=null

RUN apt update && apt install python3.5 python3-pip -y
RUN pip3 install pip --upgrade

ADD . /root
WORKDIR /root/
RUN pip3 install -r requirements.txt --upgrade
RUN pip3 install dist/moon_utilities-1.3.0-py3-none-any.whl --upgrade
RUN pip3 install .

CMD ["python3", "-m", "moon_authz"]