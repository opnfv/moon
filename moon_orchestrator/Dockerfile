FROM python:3

ADD . /root
WORKDIR /root/
RUN pip3 install -r requirements.txt
RUN pip3 install .

CMD ["python3", "-m", "moon_orchestrator"]