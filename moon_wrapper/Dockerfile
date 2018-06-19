FROM python:3

LABEL Name=Wrapper
LABEL Description="Wrapper component for the Moon platform"
LABEL Maintainer="Thomas Duval"
LABEL Url="https://wiki.opnfv.org/display/moon/Moon+Project+Proposal"

USER root

ADD . /root
WORKDIR /root/
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --no-cache-dir .

CMD ["python3", "-m", "moon_wrapper"]
