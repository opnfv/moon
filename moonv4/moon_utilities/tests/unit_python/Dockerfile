FROM python:3

RUN pip install pytest requests_mock requests --upgrade
ADD requirements.txt /root
RUN pip install -r /root/requirements.txt --upgrade

CMD ["sh", "/data/tests/unit_python/run_tests.sh"]