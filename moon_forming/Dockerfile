FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade requests pyyaml python_moonutilities python_moondb python_moonclient

ENV POPULATE_ARGS "-v"

ADD . /root
WORKDIR /root

CMD sh /root/run.sh ${POPULATE_ARGS}