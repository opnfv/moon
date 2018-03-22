FROM python:3

ADD . /root
WORKDIR /root/
RUN pip3 install -r requirements.txt
RUN if [ -d /root/dist ]; then for FILE in $(ls /root/dist/*.tar.gz); do pip install $FILE --upgrade; done; fi
RUN if [ -d /root/dist ]; then for FILE in $(ls /root/dist/*.whl); do pip install $FILE --upgrade; done; fi
RUN pip3 install .

CMD ["python3", "-m", "moon_interface"]