FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade requests pyyaml moon_utilities moon_db

ADD . /root
WORKDIR /root

CMD ["sh", "/root/run.sh" ]