FROM ubuntu:latest

RUN apt update && apt install python3.5 python3-pip -y
RUN pip3 install pip --upgrade

ADD . /root
WORKDIR /root/
RUN pip3 install -r requirements.txt
#RUN pip3 install /root/dist/* --upgrade
RUN pip3 install .

CMD ["python3", "-m", "moon_manager"]