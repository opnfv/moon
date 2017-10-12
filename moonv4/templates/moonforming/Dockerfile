FROM python:3
WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade requests pyyaml moon_utilities moon_db

ADD conf2consul.py /root
ADD run.sh /root

CMD ["bash", "/root/run.sh" ]