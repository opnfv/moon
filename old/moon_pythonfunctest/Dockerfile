FROM python:3

WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade requests pytest pyyaml python_moonutilities python_moondb python_moonclient

ADD . /root
WORKDIR /root

CMD /bin/bash /root/run_func_test.sh 
