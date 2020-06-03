FROM python:3


LABEL Name=Forming
LABEL Description="Configuration job for the Moon platform"
LABEL Maintainer="Thomas Duval"
LABEL Url="https://wiki.opnfv.org/display/moon/Moon+Project+Proposal"

USER root

WORKDIR /usr/src/app
RUN pip install --no-cache-dir --upgrade requests pytest pyyaml python_moonutilities python_moondb python_moonclient

ADD . /root
WORKDIR /root

CMD /bin/bash /root/config_moon.sh 
