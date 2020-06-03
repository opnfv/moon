FROM python:3

ADD . /root
RUN pip install -r /root/requirements.txt --upgrade
WORKDIR /root
RUN pip install .

CMD ["python", "-m", "moon_bouchon"]