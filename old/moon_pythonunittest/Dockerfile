FROM python:3

RUN pip install pytest requests_mock requests --upgrade
ADD requirements.txt /root
RUN pip install -r /root/requirements.txt --upgrade

ADD run_tests.sh /root
CMD ["sh", "/root/run_tests.sh"]